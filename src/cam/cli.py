import argparse

from .api import CAMSoftware
from .models import CAMJobConfig, MachineType, ToolConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert CAD files to CNC G-code.")
    parser.add_argument("input_file", help="Path to CAD file (.stl, .obj)")
    parser.add_argument("output_file", help="Path to output G-code file")
    parser.add_argument(
        "--machine",
        choices=[machine.value for machine in MachineType],
        default=MachineType.MILL_3_AXIS.value,
        help="Machine type",
    )
    parser.add_argument("--tool-number", type=int, default=1)
    parser.add_argument("--tool-diameter", type=float, default=6.0)
    parser.add_argument("--feed-rate", type=float, default=500.0)
    parser.add_argument("--spindle-rpm", type=int, default=6000)
    parser.add_argument("--safe-z", type=float, default=5.0)
    parser.add_argument("--cut-depth", type=float, default=1.0)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    cam = CAMSoftware()
    job = CAMJobConfig(
        machine_type=MachineType(args.machine),
        safe_z=args.safe_z,
        cut_depth=args.cut_depth,
    )
    tool = ToolConfig(
        tool_number=args.tool_number,
        diameter=args.tool_diameter,
        spindle_rpm=args.spindle_rpm,
        feed_rate=args.feed_rate,
    )
    cam.export_gcode(file_path=args.input_file, job=job, tool=tool, output_path=args.output_file)


if __name__ == "__main__":
    main()
