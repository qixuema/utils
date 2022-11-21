import os
import open3d as o3d
import numpy as np
import trimesh

# 我们直接把mesh 除以 64 * 10, 那么整个场景就归一化到 1*1*1 里面了
input_dir = "E:\\studio\\project\\Stop-motion-OBJ\\L7_seq\\L7_seq_rescale" #文件夹目录
output_dir = "E:\\studio\\project\\Stop-motion-OBJ\\L7_seq\\L7_seq_rescale_rotated"

mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
# mesh_r = copy.deepcopy(mesh).translate((2,0,0))
mesh.rotate(mesh.get_rotation_matrix_from_xyz((np.pi/2,0,np.pi/4)))
o3d.visualization.draw_geometries(mesh)