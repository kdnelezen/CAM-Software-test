from dataclasses import dataclass
from typing import List, Tuple

Point3D = Tuple[float, float, float]
LineMove = Tuple[float, float, float]


@dataclass
class MeshData:
    vertices: List[Point3D]
    faces: List[Tuple[int, ...]]
