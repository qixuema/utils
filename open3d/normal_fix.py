import open3d as o3d
import trimesh
import numpy as np

input_mesh_path = "./open3d/kitti_undc_rotated.obj"
input_points_path = "./open3d/kitti_rotated.ply"
save_path = "./open3d/output_kitti_undc_noisypc_rotated_4.obj"

input_mesh = trimesh.load(input_mesh_path)
vertices = input_mesh.vertices.astype(np.float32)
triangles = input_mesh.faces.astype(np.int32)
vertices_normal = np.zeros_like(vertices)

point_cloud_data = o3d.io.read_point_cloud(input_points_path)
# 然后，我们把输入点云transform到和输入mesh同一个坐标系下（为什么这么做呢，因为逆过程不可知）
input_points = np.asarray(point_cloud_data.points)
input_normals = np.asarray(point_cloud_data.normals)
input_ptp = input_points.ptp(axis=0)
scale_value = input_ptp.max()
input_points / scale_value
bb_min = input_points.min(axis=0)
input_points = (input_points - bb_min) / scale_value * 4 * 32

# pcd_od3 = o3d.geometry.PointCloud()
# pcd_od3.points = o3d.utility.Vector3dVector(input_points)
# pcd_od3.normals = o3d.utility.Vector3dVector(input_normals)
# o3d.io.write_point_cloud("./open3d/scaled_input_points.ply", pcd_od3)

# pcd_od3_tri = o3d.geometry.PointCloud()
# pcd_od3_tri.points = o3d.utility.Vector3dVector(vertices)
# o3d.io.write_point_cloud("./open3d/trimesh_points.ply", pcd_od3_tri)

# input_ptp = input_points.ptp(axis=0)
# vertex_ptp = vertices.ptp(axis=0)
# point_cloud_data.points = o3d.utility.Vector3dVector(input_points)
# 然后，我们构建一个 KNN 树
pcd_tree = o3d.geometry.KDTreeFlann(point_cloud_data)
vertices_size = len(vertices)
for i in range(0, vertices_size):            
    # find 10 points that closed to point_temp
    [k, idx, _] = pcd_tree.search_knn_vector_3d(vertices[i], 50)
    # 然后利用KNN 计算每一个 vertex 周围 K 个点云的法向量
    neighbor_normals = input_normals[idx]
    # 对这K 个法向量进行取平均
    mean_normal=neighbor_normals.mean(axis=0)
    # 将平均值赋值给当前的vertex
    vertices_normal[i] = mean_normal
    
fout = open(save_path, 'w')
for ii in range(len(vertices)):
    # 将 vn 写入到文件中
    # fout.write("vn "+str(vertices_normal[ii,0])+" "+str(vertices_normal[ii,1])+" "+str(vertices_normal[ii,2])+"\n")
    fout.write("v "+str(vertices[ii,0])+" "+str(vertices[ii,1])+" "+str(vertices[ii,2])+"\n")
for ii in range(len(triangles)):
    # reverse the order of triangle
    A_idx = triangles[ii,0]
    B_idx = triangles[ii,1]
    C_idx = triangles[ii,2]

    A_n = vertices_normal[A_idx]
    B_n = vertices_normal[B_idx]
    C_n = vertices_normal[C_idx]
    # 计算 A、B、C三个点的法向量均值
    mean_n = (A_n + B_n + C_n)/3
    A = vertices[A_idx]
    B = vertices[B_idx]
    C = vertices[C_idx]
    ab = B - A
    bc = C - B
    f_n = np.array([ab[1]*bc[2] -ab[2]*bc[1], ab[2]*bc[0] -ab[0]*bc[2], ab[0]*bc[1] -ab[1]*bc[0]])
    res = f_n[0]*mean_n[0] +  f_n[1]*mean_n[1] +  f_n[2]*mean_n[2]
    if res < 0:
        fout.write("f "+str(int(triangles[ii,0]+1))+" "+str(int(triangles[ii,2]+1))+" "+str(int(triangles[ii,1]+1))+"\n")
    else:
        fout.write("f "+str(int(triangles[ii,0]+1))+" "+str(int(triangles[ii,1]+1))+" "+str(int(triangles[ii,2]+1))+"\n")
fout.close()