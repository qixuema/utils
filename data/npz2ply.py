import open3d as o3d
import numpy as np


pcd_np = np.load("data/datasets/points.npz")
pcd_od3 = o3d.geometry.PointCloud()
pcd_o3d_points = pcd_np['points']

pcd_od3.points = o3d.utility.Vector3dVector(pcd_o3d_points[:, 0:3])
# pcd_od3.normals = o3d.utility.Vector3dVector(pcd_np[:, 3:6])
o3d.io.write_point_cloud("data/datasets/points.ply", pcd_od3)