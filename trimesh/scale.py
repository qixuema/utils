import os
# import open3d as o3d
import numpy as np
import trimesh

# 我们直接把mesh 除以 64 * 10, 那么整个场景就归一化到 1*1*1 里面了
input_dir = "E:\\studio\\project\\Stop-motion-OBJ\\L7_seq\\L7_seq" #文件夹目录
output_dir = "E:\\studio\\project\\Stop-motion-OBJ\\L7_seq\\L7_seq_rescale"

def rescale_mesh(file_name):
    input_mesh = trimesh.load(input_dir +"\\"+ file_name)
    input_vertices = input_mesh.vertices.astype(np.float32)
    input_triangles = input_mesh.faces.astype(np.int32)
    
    input_vertices =  input_vertices / 640
    
    save_mesh_path = output_dir +"\\"+ file_name
    fout = open(save_mesh_path, 'w')
    for ii in range(len(input_vertices)):
        fout.write("v "+str(input_vertices[ii,0])+" "+str(input_vertices[ii,1])+" "+str(input_vertices[ii,2])+"\n")

    for ii in range(len(input_triangles)):
        fout.write("f "+str(int(input_triangles[ii,0]+1))+" "+str(int(input_triangles[ii,1]+1))+" "+str(int(input_triangles[ii,2]+1))+"\n")
    fout.close()

# output_mesh_dir = "./open3d/output_data/L7_seq"
files= os.listdir(input_dir) #得到文件夹下的所有文件名称
files = sorted(files)
a = 0
for file_name in files:
    save_mesh_path = output_dir +"\\"+ file_name
    if os.path.exists(save_mesh_path):
        continue
    print(file_name)
    rescale_mesh(file_name)