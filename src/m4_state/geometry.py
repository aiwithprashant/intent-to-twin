import open3d as o3d


def extract_geometry(mesh_path):
    mesh = o3d.io.read_triangle_mesh(mesh_path)

    bbox = mesh.get_axis_aligned_bounding_box()

    return {
        "num_vertices": len(mesh.vertices),
        "num_triangles": len(mesh.triangles),
        "bbox_min": bbox.min_bound.tolist(),
        "bbox_max": bbox.max_bound.tolist()
    }