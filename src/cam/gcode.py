from typing import Iterable, List

from .models import CAMJobConfig, MachineType, ToolConfig
from .toolpath import ToolPath


class GCodeGenerator:
    def generate(self, paths: Iterable[ToolPath], job: CAMJobConfig, tool: ToolConfig) -> str:
        gcode: List[str] = [
            "%",
            f"(Machine: {job.machine_type.value})",
            "G21" if job.units.lower() == "mm" else "G20",
            "G90",
            "G17",
            f"T{tool.tool_number} M6",
            f"S{tool.spindle_rpm} M3",
            f"F{tool.feed_rate:.3f}",
        ]

        if job.machine_type == MachineType.LATHE_2_AXIS:
            gcode.append("G18")

        for path in paths:
            gcode.append(f"(Strategy: {path.strategy})")
            for i, (x, y, z) in enumerate(path.moves):
                if i == 0 or z >= 0:
                    command = "G0"
                else:
                    command = "G1"
                gcode.append(f"{command} X{x:.4f} Y{y:.4f} Z{z:.4f}")

        gcode.extend(["M5", "G0 Z10.0000", "M30", "%"])
        return "\n".join(gcode)
