import open3d as o3d
import numpy as np

input_mesh_path = "open3d/data/output_data/god-knows.ply"
output_mesh_path = "open3d/data/output_data/god-knows-centra.ply"
mesh = o3d.io.read_triangle_mesh(input_mesh_path)
vertices = np.asarray(mesh.vertices)


# 计算极差值，即波峰到波谷
vertices_ptp = vertices.ptp(axis=0) 
# scale_value = vertices_ptp.max()
# bb_min = vertices.min(axis=0)
input_points = vertices - vertices_ptp/2
mesh.vertices = o3d.utility.Vector3dVector(input_points)
o3d.io.write_triangle_mesh(output_mesh_path, mesh)