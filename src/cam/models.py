from dataclasses import dataclass
from enum import Enum


class MachineType(str, Enum):
    MILL_2_AXIS = "2_axis_mill"
    MILL_3_AXIS = "3_axis_mill"
    MILL_4_AXIS = "4_axis_mill"
    LATHE_2_AXIS = "2_axis_lathe"


@dataclass(frozen=True)
class ToolConfig:
    tool_number: int = 1
    diameter: float = 6.0
    spindle_rpm: int = 6000
    feed_rate: float = 500.0
    plunge_rate: float = 200.0


@dataclass(frozen=True)
class CAMJobConfig:
    machine_type: MachineType
    safe_z: float = 5.0
    cut_depth: float = 1.0
    stepover_ratio: float = 0.5
    units: str = "mm"
