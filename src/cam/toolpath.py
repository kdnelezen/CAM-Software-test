from dataclasses import dataclass
from typing import List, Tuple

from .geometry import MeshAnalysis
from .models import CAMJobConfig, MachineType, ToolConfig

Move = Tuple[float, float, float]


@dataclass(frozen=True)
class ToolPath:
    strategy: str
    moves: List[Move]


class ToolPathGenerator:
    def generate(self, analysis: MeshAnalysis, job: CAMJobConfig, tool: ToolConfig) -> List[ToolPath]:
        if not analysis.is_valid:
            raise ValueError("Cannot generate tool path for invalid mesh")

        roughing = ToolPath(strategy="roughing", moves=self._roughing_pass(analysis, job, tool))
        finishing = ToolPath(strategy="finishing", moves=self._finishing_pass(analysis, job, tool))
        adaptive = ToolPath(strategy="adaptive", moves=self._adaptive_pass(analysis, job, tool))
        return [roughing, finishing, adaptive]

    def _roughing_pass(self, analysis: MeshAnalysis, job: CAMJobConfig, tool: ToolConfig) -> List[Move]:
        min_x, min_y, _ = analysis.bounds_min
        max_x, max_y, _ = analysis.bounds_max
        step = max(tool.diameter * job.stepover_ratio, 0.1)
        depth = -abs(job.cut_depth)

        rows: List[Move] = [(min_x, min_y, job.safe_z), (min_x, min_y, depth)]
        y = min_y
        direction = 1
        while y <= max_y:
            target_x = max_x if direction > 0 else min_x
            rows.append((target_x, y, depth))
            y += step
            rows.append((target_x, min(y, max_y), depth))
            direction *= -1
        rows.append((rows[-1][0], rows[-1][1], job.safe_z))
        return rows

    def _finishing_pass(self, analysis: MeshAnalysis, job: CAMJobConfig, tool: ToolConfig) -> List[Move]:
        min_x, min_y, _ = analysis.bounds_min
        max_x, max_y, _ = analysis.bounds_max
        depth = -abs(job.cut_depth)
        return [
            (min_x, min_y, job.safe_z),
            (min_x, min_y, depth),
            (max_x, min_y, depth),
            (max_x, max_y, depth),
            (min_x, max_y, depth),
            (min_x, min_y, depth),
            (min_x, min_y, job.safe_z),
        ]

    def _adaptive_pass(self, analysis: MeshAnalysis, job: CAMJobConfig, tool: ToolConfig) -> List[Move]:
        min_x, min_y, _ = analysis.bounds_min
        max_x, max_y, _ = analysis.bounds_max
        cx = (min_x + max_x) / 2.0
        cy = (min_y + max_y) / 2.0
        depth = -abs(job.cut_depth) * 0.7

        if job.machine_type == MachineType.LATHE_2_AXIS:
            return [
                (min_x, cy, job.safe_z),
                (max_x, cy, depth),
                (min_x, cy, depth),
                (min_x, cy, job.safe_z),
            ]

        if job.machine_type == MachineType.MILL_4_AXIS:
            return [
                (cx, cy, job.safe_z),
                (max_x, cy, depth),
                (cx, max_y, depth),
                (min_x, cy, depth),
                (cx, min_y, depth),
                (cx, cy, job.safe_z),
            ]

        return [
            (cx, min_y, job.safe_z),
            (max_x, cy, depth),
            (cx, max_y, depth),
            (min_x, cy, depth),
            (cx, min_y, job.safe_z),
        ]
