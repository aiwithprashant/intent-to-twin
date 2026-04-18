import open3d as o3d
import numpy as np
from pathlib import Path


class ReconstructionEngine:
    def __init__(self):
        pass

    def reconstruct(self, image_paths, output_path):
        # Placeholder mesh (replace later with TripoSR)
        mesh = o3d.geometry.TriangleMesh.create_sphere(radius=1.0)
        mesh.compute_vertex_normals()

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        o3d.io.write_triangle_mesh(output_path, mesh)

        return output_path