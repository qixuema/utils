import os
from plyfile import PlyElement, PlyData
import numpy as np

def load_pointcloud(in_file):
    plydata = PlyData.read(in_file)
    vertices = np.stack([
        plydata['vertex']['x'],
        plydata['vertex']['y'],
        plydata['vertex']['z']
    ], axis=1)
    normals = np.stack([
       plydata['vertex']['nx'],
       plydata['vertex']['ny'],
       plydata['vertex']['nz']
    ], axis=1)
    return vertices, normals

pointcloud, normals= load_pointcloud("data/factory/obj/factory-10m-mini.ply")
np.savez("factory-10m-mini.npz", points=pointcloud, normals=normals)