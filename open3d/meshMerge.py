# import open3d as o3d
import os
import numpy as np
import trimesh


def save_mesh(save_path, save_mesh):
    combined_vertices = save_mesh.vertices.astype(np.float32)
    combined_triangles = save_mesh.faces.astype(np.int32)
    
    save_mesh_path = save_path
    fout = open(save_mesh_path, 'w')
    for ii in range(len(combined_vertices)):
        fout.write("v "+str(combined_vertices[ii,0])+" "+str(combined_vertices[ii,1])+" "+str(combined_vertices[ii,2])+"\n")

    for ii in range(len(combined_triangles)):
            fout.write("f "+str(int(combined_triangles[ii,0]+1))+" "+str(int(combined_triangles[ii,1]+1))+" "+str(int(combined_triangles[ii,2]+1))+"\n")
    fout.close()

first_mesh_path = "./open3d/input_data/L7_seq/0001.obj"
combined = trimesh.load(first_mesh_path)


# second_mesh_path = "./open3d/input_data/L7_seq/L7_(228).obj"
# second_mesh = trimesh.load(second_mesh_path)

# combined = trimesh.util.concatenate( [ combined, second_mesh ] )
# output_mesh_path = "./open3d/output_data/L7_seq/L7_"+str(228)+".obj"
# save_mesh(output_mesh_path, combined)


input_dir = "/root/studio/project/utils_ma/utils/open3d/input_data/L7_seq" #文件夹目录
output_mesh_dir = "./open3d/output_data/L7_seq"
files= os.listdir(input_dir) #得到文件夹下的所有文件名称
files = sorted(files)
for file_name in files:
    if file_name == "0001.obj":
        continue
    input_mesh_append = trimesh.load(input_dir + "/"+ file_name)
    
    combined = trimesh.util.concatenate( [ combined, input_mesh_append ] )
    output_mesh_path = output_mesh_dir + "/" + file_name
    save_mesh(output_mesh_path, combined)

# for i in range (2,229):
#     # combined_mesh
    
#     input_mesh_path_append = "./open3d/input_data/L7_seq/L7_("+str(i)+").obj"
#     input_mesh_append = trimesh.load(input_mesh_path_append)
    
#     combined = trimesh.util.concatenate( [ combined, input_mesh_append ] )
#     output_mesh_dir = "./open3d/output_data/L7_seq/L7_"+str(i)+".obj"
#     save_mesh(output_mesh_dir, combined)
    
    