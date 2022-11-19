import open3d as o3d
import numpy as np

input_file = "./data/input_data/out.npy"
output_file = "./data/output_data/out_1.ply"
pcd_np = np.load(input_file)
pcd_od3 = o3d.geometry.PointCloud()
pcd_od3.points = o3d.utility.Vector3dVector(pcd_np[1, :, 0:3])
# pcd_od3.normals = o3d.utility.Vector3dVector(pcd_np[0, :, 3:6])
o3d.io.write_point_cloud(output_file, pcd_od3)