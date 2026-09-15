import os
import struct
from abc import ABC, abstractmethod
from typing import Dict, Iterable, List, Tuple

from .types import MeshData, Point3D


class CADParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> MeshData:
        raise NotImplementedError


class STLParser(CADParser):
    def parse(self, file_path: str) -> MeshData:
        with open(file_path, "rb") as source:
            payload = source.read()

        if self._looks_ascii(payload):
            return self._parse_ascii(payload.decode("utf-8", errors="ignore").splitlines())
        return self._parse_binary(payload)

    @staticmethod
    def _looks_ascii(payload: bytes) -> bool:
        if len(payload) < 84:
            return True
        if not payload.startswith(b"solid"):
            return False
        triangle_count = struct.unpack("<I", payload[80:84])[0]
        expected_binary_size = 84 + triangle_count * 50
        return len(payload) != expected_binary_size

    @staticmethod
    def _parse_ascii(lines: Iterable[str]) -> MeshData:
        vertices: List[Point3D] = []
        faces: List[Tuple[int, ...]] = []
        cache: Dict[Point3D, int] = {}
        current: List[int] = []

        for line in lines:
            stripped = line.strip()
            if not stripped.startswith("vertex "):
                continue
            _, x, y, z = stripped.split(maxsplit=3)
            point = (float(x), float(y), float(z))
            if point not in cache:
                cache[point] = len(vertices)
                vertices.append(point)
            current.append(cache[point])
            if len(current) == 3:
                faces.append(tuple(current))
                current = []
        return MeshData(vertices=vertices, faces=faces)

    @staticmethod
    def _parse_binary(payload: bytes) -> MeshData:
        triangle_count = struct.unpack("<I", payload[80:84])[0]
        offset = 84
        vertices: List[Point3D] = []
        faces: List[Tuple[int, ...]] = []
        cache: Dict[Point3D, int] = {}

        for _ in range(triangle_count):
            offset += 12  # Skip normal vector
            indices: List[int] = []
            for _ in range(3):
                x, y, z = struct.unpack("<fff", payload[offset : offset + 12])
                offset += 12
                point = (float(x), float(y), float(z))
                if point not in cache:
                    cache[point] = len(vertices)
                    vertices.append(point)
                indices.append(cache[point])
            faces.append(tuple(indices))
            offset += 2  # attribute byte count
        return MeshData(vertices=vertices, faces=faces)


class OBJParser(CADParser):
    def parse(self, file_path: str) -> MeshData:
        vertices: List[Point3D] = []
        faces: List[Tuple[int, ...]] = []

        with open(file_path, "r", encoding="utf-8") as source:
            for raw_line in source:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("v "):
                    _, x, y, z = line.split(maxsplit=3)
                    vertices.append((float(x), float(y), float(z)))
                elif line.startswith("f "):
                    chunks = line.split()[1:]
                    indices: List[int] = []
                    for chunk in chunks:
                        base = chunk.split("/")[0]
                        idx = int(base)
                        if idx < 0:
                            idx = len(vertices) + idx + 1
                        indices.append(idx - 1)
                    faces.append(tuple(indices))
        return MeshData(vertices=vertices, faces=faces)


class ParserRegistry:
    def __init__(self) -> None:
        self._parsers: Dict[str, CADParser] = {
            ".stl": STLParser(),
            ".obj": OBJParser(),
        }

    def register_parser(self, extension: str, parser: CADParser) -> None:
        self._parsers[extension.lower()] = parser

    def parse(self, file_path: str) -> MeshData:
        extension = os.path.splitext(file_path)[1].lower()
        parser = self._parsers.get(extension)
        if parser is None:
            supported = ", ".join(sorted(self._parsers.keys()))
            raise ValueError(f"Unsupported CAD format '{extension}'. Supported formats: {supported}")
        return parser.parse(file_path)
