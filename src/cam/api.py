from dataclasses import asdict
from pathlib import Path
from typing import Dict, List

from .gcode import GCodeGenerator
from .geometry import GeometryProcessor
from .models import CAMJobConfig, ToolConfig
from .parsers import ParserRegistry
from .toolpath import ToolPath, ToolPathGenerator


class CAMSoftware:
    def __init__(self) -> None:
        self.parsers = ParserRegistry()
        self.geometry_processor = GeometryProcessor()
        self.toolpath_generator = ToolPathGenerator()
        self.gcode_generator = GCodeGenerator()

    def supported_formats(self) -> List[str]:
        return sorted(self.parsers._parsers.keys())  # noqa: SLF001

    def convert_to_gcode(self, file_path: str, job: CAMJobConfig, tool: ToolConfig) -> str:
        mesh = self.parsers.parse(file_path)
        analysis = self.geometry_processor.analyze_mesh(mesh)
        if not analysis.is_valid:
            raise ValueError(f"Invalid geometry: {', '.join(analysis.issues)}")
        paths = self.toolpath_generator.generate(analysis, job, tool)
        return self.gcode_generator.generate(paths, job, tool)

    def export_gcode(self, file_path: str, job: CAMJobConfig, tool: ToolConfig, output_path: str) -> str:
        gcode = self.convert_to_gcode(file_path=file_path, job=job, tool=tool)
        Path(output_path).write_text(gcode, encoding="utf-8")
        return output_path

    def preview_job(self, file_path: str, job: CAMJobConfig, tool: ToolConfig) -> Dict[str, object]:
        mesh = self.parsers.parse(file_path)
        analysis = self.geometry_processor.analyze_mesh(mesh)
        paths: List[ToolPath] = self.toolpath_generator.generate(analysis, job, tool) if analysis.is_valid else []
        return {
            "job": asdict(job),
            "tool": asdict(tool),
            "geometry_valid": analysis.is_valid,
            "geometry_issues": analysis.issues,
            "toolpath_strategies": [path.strategy for path in paths],
            "toolpath_move_counts": {path.strategy: len(path.moves) for path in paths},
        }
