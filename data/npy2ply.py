import open3d as o3d
import numpy as np


pcd_np = np.load("../data/gibson_tiny/Coffeen/scene2M.npy")
pcd_od3 = o3d.geometry.PointCloud()
pcd_od3.points = o3d.utility.Vector3dVector(pcd_np[:, 0:3])
pcd_od3.normals = o3d.utility.Vector3dVector(pcd_np[:, 3:6])
o3d.io.write_point_cloud("../data/gibson_tiny/Coffeen/scene2M.ply", pcd_od3)