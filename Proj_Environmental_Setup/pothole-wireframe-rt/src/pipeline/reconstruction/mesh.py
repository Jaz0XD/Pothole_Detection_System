from open3d import geometry, io

def generate_mesh_from_point_cloud(point_cloud):
    """
    Generates a 3D mesh from a given point cloud using Poisson reconstruction.

    Args:
        point_cloud (open3d.geometry.PointCloud): The input point cloud.

    Returns:
        open3d.geometry.TriangleMesh: The generated mesh.
    """
    # Estimate normals
    point_cloud.estimate_normals(search_param=geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    
    # Perform Poisson reconstruction
    mesh, densities = geometry.TriangleMesh.create_from_point_cloud_poisson(point_cloud, depth=9)
    
    # Remove low-density vertices
    vertices_to_remove = densities < densities.mean()
    mesh.remove_vertices_by_mask(vertices_to_remove)

    return mesh

def save_mesh(mesh, filename):
    """
    Saves the generated mesh to a file.

    Args:
        mesh (open3d.geometry.TriangleMesh): The mesh to save.
        filename (str): The filename for the output mesh.
    """
    io.write_triangle_mesh(filename, mesh)

def load_point_cloud(filename):
    """
    Loads a point cloud from a file.

    Args:
        filename (str): The filename of the point cloud.

    Returns:
        open3d.geometry.PointCloud: The loaded point cloud.
    """
    return io.read_point_cloud(filename)

# Example usage
if __name__ == "__main__":
    point_cloud = load_point_cloud("path/to/point_cloud.ply")
    mesh = generate_mesh_from_point_cloud(point_cloud)
    save_mesh(mesh, "output_mesh.ply")