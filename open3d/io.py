from turtle import shape
import open3d as o3d
import numpy as np


file_name = "./open3d/input_data/bunny.ply"
cloud = o3d.io.read_point_cloud(file_name)
input_points = np.asarray(cloud.points)

input_points_shape = input_points.shape
print(input_points_shape)
dp = input_points[0]
print(dp)
