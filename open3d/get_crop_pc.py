# import os
import open3d as o3d
import numpy as np

input_ply_path = './open3d/data/input_data/L7_100K_normal.ply'
# read ply file
pcd = o3d.io.read_point_cloud(input_ply_path)


input_points = np.asarray(pcd.points)
input_normals = np.asarray(pcd.normals)
LOD_input = input_points

block_num_per_dim = 10
output_grid_size = 64
block_padding = 5
input_point_num = 16384
write_text = True


#normalize to unit cube for each crop
LOD_input_min = np.min(LOD_input,0)
LOD_input_max = np.max(LOD_input,0)
LOD_input_scale = np.max(LOD_input_max-LOD_input_min)
LOD_input = LOD_input-np.reshape(LOD_input_min, [1,3])
LOD_input = LOD_input/(LOD_input_scale/block_num_per_dim)
full_scene = LOD_input
full_scene_size = np.ceil(np.max(full_scene,0)).astype(np.int32)
print("Crops:", full_scene_size)
full_scene = full_scene*output_grid_size

input_data = np.concatenate((full_scene, input_normals), axis=1)



index = 0

def get_crop_pc(index):
    idx_x = index//(full_scene_size[1]*full_scene_size[2])
    idx_yz = index%(full_scene_size[1]*full_scene_size[2])
    idx_y = idx_yz//full_scene_size[2]
    idx_z = idx_yz%full_scene_size[2]

    gt_input_mask_ = \
        (input_data[:,0]> idx_x    *output_grid_size-block_padding) & \
        (input_data[:,0]< (idx_x+1)*output_grid_size+block_padding) & \
        (input_data[:,1]> idx_y    *output_grid_size-block_padding) & \
        (input_data[:,1]< (idx_y+1)*output_grid_size+block_padding) & \
        (input_data[:,2]> idx_z    *output_grid_size-block_padding) & \
        (input_data[:,2]< (idx_z+1)*output_grid_size+block_padding)

    if np.sum(gt_input_mask_)<100:
        # return np.zeros([1],np.float32),np.zeros([1],np.float32),np.zeros([1],np.float32),np.zeros([1],np.float32),np.zeros([1],np.float32)
        return

    gt_input_ = input_data[gt_input_mask_]
    # gt_input_ = input_points - \
    #     np.array([[
    #         idx_x*output_grid_size-block_padding, 
    #         idx_y*output_grid_size-block_padding, 
    #         idx_z*output_grid_size-block_padding]], np.float32)

    np.random.shuffle(gt_input_)
    gt_input_ = gt_input_[:input_point_num]
    gt_input_ = np.ascontiguousarray(gt_input_)

    # write_ply_point(str(index)+".ply", gt_input_)
    # write ply file
    output_pcd = o3d.geometry.PointCloud()
    output_pcd.points = o3d.utility.Vector3dVector(gt_input_[:, 0:3])
    output_pcd.normals = o3d.utility.Vector3dVector(gt_input_[:, 3:6])    
    output_ply_path = "./open3d/data/output_data/"+str(index)+".ply"
    o3d.io.write_point_cloud(output_ply_path, output_pcd, write_ascii=write_text)
    
    poisson_mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(output_pcd, depth=10, width=0, scale=1.1, linear_fit=False)

    # min_density = 0.1
    # vertices_to_remove = densities < np.quantile(densities, min_density)
    # poisson_mesh.remove_vertices_by_mask(vertices_to_remove)
    
    bbox = output_pcd.get_axis_aligned_bounding_box() 
    poisson_mesh = poisson_mesh.crop(bbox)
    
    output_mesh_path = "./open3d/data/output_data/mesh-"+str(index)+".ply"
    o3d.io.write_triangle_mesh(output_mesh_path, poisson_mesh, write_ascii=True)

full_size = full_scene_size[0]*full_scene_size[1]*full_scene_size[2]
for i in range(full_size):
    get_crop_pc(i)


