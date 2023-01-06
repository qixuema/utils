import open3d as o3d

path = "/root/studio/tmp/fusion/SingleFrame"

for i in range(1,157):
    input_path = path + "/sf_" + str(i).zfill(4)+"_mesh.ply"
    mesh = o3d.io.read_triangle_mesh(input_path)
    output_path = path + "/mesh_obj/sf_" + str(i).zfill(4)+"_mesh.obj"
    o3d.io.write_triangle_mesh(output_path, mesh, write_triangle_uvs=True)