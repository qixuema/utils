# from math import ceil
# print(ceil(110/10))

import open3d as o3d
import multiprocessing as mp
import numpy as np

input_point_path = "./open3d/map_pc.ply"
point_cloud_data = o3d.io.read_point_cloud(input_point_path)

vertices = np.random.rand(100,3)
# print(vertices)
triangles = np.random.randint(0,10,size=(150,3))
# print(triangles)
vertices_normal = np.zeros_like(vertices)
# print(vertices_normal)
pcd = o3d.geometry.PointCloud()
input_points = np.random.rand(100,6)
# 然后，我们把输入点云transform到和输入mesh同一个坐标系下（为什么这么做呢，因为逆过程不可知）
bb_min = input_points[:,0:3].min(axis=0)
input_points[:,0:3] = (input_points[:,0:3] - bb_min) * 10
# print(input_points)
pcd.points = o3d.utility.Vector3dVector(input_points[:,0:3])
# pcd.normals = o3d.utility.Vector3dVector(input_points[:,3:6])
input_normals = input_points[:,3:6]


def compute_normal(pcd_tree, vertices, input_normals,vertices_normal, ii,jj):
    for i in range(ii,jj):    
        # find 10 points that closed to point_temp
        [k, idx, _] = pcd_tree.search_knn_vector_3d(vertices[i], 10)
        # 然后利用KNN 计算每一个 vertex 周围 K 个点云的法向量
        neighbor_normals = input_normals[idx]
        # 对这K 个法向量进行取平均
        mean_normal=neighbor_normals.mean(axis=0)
        # 将平均值赋值给当前的vertex
        vertices_normal[i]=mean_normal
        
def write_obj_triangle_with_normal(vertices, triangles, point_cloud_data, input_normals):

    vertices_normal = np.zeros_like(vertices)
    # 在这里，我们把原始输入点云的法向量也放进来，
    # point_cloud_data = o3d.io.read_point_cloud(input_points)

   # 然后，我们构建一个 KNN 树
    pcd_tree = o3d.geometry.KDTreeFlann(point_cloud_data)
    vertices_size = len(vertices)

    for i in range(0, vertices_size):            
            # find 10 points that closed to point_temp
            [k, idx, _] = pcd_tree.search_knn_vector_3d(vertices[i], 10)
            # 然后利用KNN 计算每一个 vertex 周围 K 个点云的法向量
            neighbor_normals = input_normals[idx]
            # 对这K 个法向量进行取平均
            mean_normal=neighbor_normals.mean(axis=0)
            # 将平均值赋值给当前的vertex
            vertices_normal[i]=mean_normal
         

    # num_cores = int(mp.cpu_count())
    # pool = mp.Pool(num_cores)
    # # param_dict = {}
    # part_size = 10

    # vertices_size_part = ceil(vertices_size / part_size)
    # ii = 0 
    # for i in range (vertices_size_part):
    #     jj = min(ii + part_size, vertices_size)
    #     pool.apply_async(compute_normal, args=(pcd_tree, vertices, input_normals,vertices_normal, ii,jj))
    #     ii += part_size
    
    # pool.close()
    # pool.join()
    # print('All subprocesses done.')

    # 将 vn 写入到文件中
    fout = open(name, 'w')
    for ii in range(len(vertices)):
        fout.write("vn "+str(vertices_normal[ii,0])+" "+str(vertices_normal[ii,1])+" "+str(vertices_normal[ii,2])+"\n")
        fout.write("v "+str(vertices[ii,0])+" "+str(vertices[ii,1])+" "+str(vertices[ii,2])+"\n")
    for ii in range(len(triangles)):
        fout.write("f "+str(int(triangles[ii,0]+1))+" "+str(int(triangles[ii,1]+1))+" "+str(int(triangles[ii,2]+1))+"\n")
    fout.close()

write_obj_triangle_with_normal(vertices,triangles,pcd, input_normals)