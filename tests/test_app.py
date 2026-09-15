import unittest

from src.cam.app import build_configs, default_output_path, machine_choices
from src.cam.models import MachineType


class DesktopAppHelperTests(unittest.TestCase):
    def test_default_output_path_replaces_existing_suffix(self) -> None:
        self.assertEqual(default_output_path("part.stl"), "part.nc")

    def test_default_output_path_adds_suffix_when_missing(self) -> None:
        self.assertEqual(default_output_path("part"), "part.nc")

    def test_build_configs_uses_existing_model_types(self) -> None:
        job, tool = build_configs("3_axis_mill", 2, 8.0, 650.0, 9000, 7.5, 2.5)
        self.assertEqual(job.machine_type, MachineType.MILL_3_AXIS)
        self.assertEqual(job.safe_z, 7.5)
        self.assertEqual(job.cut_depth, 2.5)
        self.assertEqual(tool.tool_number, 2)
        self.assertEqual(tool.diameter, 8.0)
        self.assertEqual(tool.feed_rate, 650.0)
        self.assertEqual(tool.spindle_rpm, 9000)

    def test_machine_choices_reflect_machine_enum(self) -> None:
        self.assertEqual(machine_choices(), [machine.value for machine in MachineType])


if __name__ == "__main__":
    unittest.main()
