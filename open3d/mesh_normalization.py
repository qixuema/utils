import open3d as o3d
import numpy as np

input_mesh_path = "open3d/data/input_data/god-knows.ply"
output_mesh_path = "open3d/data/output_data/god-knows.ply"
mesh = o3d.io.read_triangle_mesh(input_mesh_path)
vertices = np.asarray(mesh.vertices)


sin_theta_90 = np.sin(np.pi/2)
cos_theta_90 = np.cos(np.pi/2)
rotate_metrix_x = np.array([[1, 0, 0],
                         [0, cos_theta_90, -sin_theta_90],
                         [0, sin_theta_90, cos_theta_90]])
vertices = np.dot(vertices, rotate_metrix_x)


sin_theta_180 = np.sin(np.pi)
cos_theta_180 = np.cos(np.pi)
rotate_metrix_y = np.array([[cos_theta_180, 0, sin_theta_180],
                         [0, 1, 0],
                         [-sin_theta_180, 0, cos_theta_180]])
vertices = np.dot(vertices, rotate_metrix_y)


# 计算极差值，即波峰到波谷
vertices_ptp = vertices.ptp(axis=0) 
scale_value = vertices_ptp.max()
bb_min = vertices.min(axis=0)
input_points = (vertices - bb_min) / scale_value
mesh.vertices = o3d.utility.Vector3dVector(input_points)
o3d.io.write_triangle_mesh(output_mesh_path, mesh)



# import numpy as np
# import open3d as o3d
# from open3d import geometry

# # Create a NumPy array with vertex coordinates and face indices
# vertex_coords = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0]])
# face_indices = np.array([[0, 1, 2], [1, 3, 2]])

# # Create a TriangleMesh object from the vertex coordinates and face indices
# tri_mesh = geometry.TriangleMesh()
# tri_mesh.vertices = o3d.utility.Vector3dVector(vertex_coords)
# tri_mesh.triangles = o3d.utility.Vector3iVector(face_indices)

# o3d.io.write_triangle_mesh(output_mesh_path, tri_mesh)
