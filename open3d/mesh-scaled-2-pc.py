import open3d as o3d
import numpy as np
import trimesh

input_mesh_path = "./open3d/data/input_data/mesh-mai.obj"
input_points_path = "./open3d/data/input_data/pc-mai.ply"
output_mesh_path = "open3d/data/output_data/mai-ori.ply"


point_cloud_data = o3d.io.read_point_cloud(input_points_path)

input_points = np.asarray(point_cloud_data.points)

# 计算极差值，即波峰到波谷
input_ptp = input_points.ptp(axis=0)
print(input_ptp)
scale_value = input_ptp.max()
print(scale_value)
bb_min = input_points.min(axis=0)
print(bb_min)


mesh = o3d.io.read_triangle_mesh(input_mesh_path)
vertices = np.asarray(mesh.vertices)
input_points = vertices/640 * scale_value + bb_min
mesh.vertices = o3d.utility.Vector3dVector(input_points)
o3d.io.write_triangle_mesh(output_mesh_path, mesh)