import numpy as np
import open3d as o3d

def create_point_cloud(depth_map, rgb_image):
    """
    Create a point cloud from a depth map and corresponding RGB image.

    Parameters:
    - depth_map: A 2D numpy array representing the depth values.
    - rgb_image: A 3D numpy array representing the RGB image.

    Returns:
    - point_cloud: An Open3D PointCloud object.
    """
    height, width = depth_map.shape
    x, y = np.meshgrid(np.arange(width), np.arange(height))
    
    # Convert depth map to point cloud
    z = depth_map
    points = np.stack((x, y, z), axis=-1).reshape(-1, 3)
    colors = rgb_image.reshape(-1, 3) / 255.0  # Normalize RGB values to [0, 1]

    # Create Open3D PointCloud
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)
    point_cloud.colors = o3d.utility.Vector3dVector(colors)

    return point_cloud

def visualize_point_cloud(point_cloud):
    """
    Visualize the point cloud using Open3D.

    Parameters:
    - point_cloud: An Open3D PointCloud object.
    """
    o3d.visualization.draw_geometries([point_cloud])

def save_point_cloud(point_cloud, filename):
    """
    Save the point cloud to a file.

    Parameters:
    - point_cloud: An Open3D PointCloud object.
    - filename: The filename to save the point cloud.
    """
    o3d.io.write_point_cloud(filename, point_cloud)

# Example usage
if __name__ == "__main__":
    # Load depth map and RGB image (dummy data for illustration)
    depth_map = np.random.rand(480, 640)  # Replace with actual depth map
    rgb_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)  # Replace with actual RGB image

    point_cloud = create_point_cloud(depth_map, rgb_image)
    visualize_point_cloud(point_cloud)
    save_point_cloud(point_cloud, "output_point_cloud.ply")