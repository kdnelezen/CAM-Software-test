import os
import struct
import tempfile
import unittest
from pathlib import Path

from src.cam import CAMJobConfig, CAMSoftware, MachineType, ToolConfig
from src.cam.parsers import ParserRegistry


ASCII_STL = """solid test
facet normal 0 0 1
outer loop
vertex 0 0 0
vertex 10 0 0
vertex 0 10 0
endloop
endfacet
endsolid test
"""

OBJ_TEXT = """v 0 0 0
v 10 0 0
v 0 10 0
f 1 2 3
"""


def _binary_stl_triangle() -> bytes:
    header = b"Binary STL Test".ljust(80, b"\x00")
    triangle_count = struct.pack("<I", 1)
    normal = struct.pack("<fff", 0.0, 0.0, 1.0)
    v1 = struct.pack("<fff", 0.0, 0.0, 0.0)
    v2 = struct.pack("<fff", 10.0, 0.0, 0.0)
    v3 = struct.pack("<fff", 0.0, 10.0, 0.0)
    attribute = struct.pack("<H", 0)
    return header + triangle_count + normal + v1 + v2 + v3 + attribute


class CAMPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.dir = Path(self.tempdir.name)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _create_file(self, name: str, content: bytes | str) -> str:
        path = self.dir / name
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
        return os.fspath(path)

    def test_parser_supports_ascii_and_binary_stl(self) -> None:
        registry = ParserRegistry()
        ascii_path = self._create_file("part_ascii.stl", ASCII_STL)
        binary_path = self._create_file("part_binary.stl", _binary_stl_triangle())

        ascii_mesh = registry.parse(ascii_path)
        binary_mesh = registry.parse(binary_path)

        self.assertEqual(len(ascii_mesh.vertices), 3)
        self.assertEqual(len(binary_mesh.vertices), 3)
        self.assertEqual(len(ascii_mesh.faces), 1)
        self.assertEqual(len(binary_mesh.faces), 1)

    def test_parser_supports_obj(self) -> None:
        registry = ParserRegistry()
        obj_path = self._create_file("part.obj", OBJ_TEXT)
        mesh = registry.parse(obj_path)
        self.assertEqual(len(mesh.vertices), 3)
        self.assertEqual(mesh.faces[0], (0, 1, 2))

    def test_supported_machine_types(self) -> None:
        machines = {machine.value for machine in MachineType}
        self.assertEqual(
            machines,
            {"2_axis_mill", "3_axis_mill", "4_axis_mill", "2_axis_lathe"},
        )

    def test_end_to_end_gcode_generation_and_export(self) -> None:
        stl_path = self._create_file("job.stl", ASCII_STL)
        out_path = self.dir / "job.nc"
        cam = CAMSoftware()
        job = CAMJobConfig(machine_type=MachineType.MILL_3_AXIS, cut_depth=2.0)
        tool = ToolConfig(tool_number=3, spindle_rpm=8000, feed_rate=650.0)

        gcode = cam.convert_to_gcode(file_path=stl_path, job=job, tool=tool)
        cam.export_gcode(file_path=stl_path, job=job, tool=tool, output_path=os.fspath(out_path))

        self.assertIn("(Machine: 3_axis_mill)", gcode)
        self.assertIn("(Strategy: roughing)", gcode)
        self.assertIn("T3 M6", gcode)
        self.assertTrue(out_path.exists())

    def test_preview_provides_strategy_and_counts(self) -> None:
        stl_path = self._create_file("preview.stl", ASCII_STL)
        cam = CAMSoftware()
        preview = cam.preview_job(
            file_path=stl_path,
            job=CAMJobConfig(machine_type=MachineType.LATHE_2_AXIS),
            tool=ToolConfig(),
        )
        self.assertTrue(preview["geometry_valid"])
        self.assertIn("roughing", preview["toolpath_strategies"])
        self.assertGreater(preview["toolpath_move_counts"]["adaptive"], 0)


if __name__ == "__main__":
    unittest.main()
