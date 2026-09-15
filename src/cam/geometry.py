from dataclasses import dataclass
from typing import List

import numpy as np

from .types import MeshData


@dataclass(frozen=True)
class MeshAnalysis:
    is_valid: bool
    bounds_min: np.ndarray
    bounds_max: np.ndarray
    dimensions: np.ndarray
    issues: List[str]


class GeometryProcessor:
    def analyze_mesh(self, mesh: MeshData) -> MeshAnalysis:
        issues: List[str] = []
        if not mesh.vertices:
            return MeshAnalysis(
                is_valid=False,
                bounds_min=np.array([0.0, 0.0, 0.0]),
                bounds_max=np.array([0.0, 0.0, 0.0]),
                dimensions=np.array([0.0, 0.0, 0.0]),
                issues=["Mesh has no vertices"],
            )

        vertices = np.array(mesh.vertices, dtype=float)
        bounds_min = vertices.min(axis=0)
        bounds_max = vertices.max(axis=0)
        dimensions = bounds_max - bounds_min

        if len(mesh.faces) == 0:
            issues.append("Mesh has no faces")
        if np.count_nonzero(dimensions > 0) < 2:
            issues.append("Mesh dimensions are degenerate")

        return MeshAnalysis(
            is_valid=not issues,
            bounds_min=bounds_min,
            bounds_max=bounds_max,
            dimensions=dimensions,
            issues=issues,
        )
