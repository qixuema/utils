import os
path = "E:\studio\project\Stop-motion-OBJ\L7_sequence" #文件夹目录
files= os.listdir(path) #得到文件夹下的所有文件名称
s = []
for file_name in files: #遍历文件夹
     if not os.path.isdir(file_name): #判断是否是文件夹，不是文件夹才打开
        # 修改文件夹的名称
        split_file_name = file_name.split('(')
        file_name_number, _ = split_file_name[1].split(')')
        # index = int(file_name_number)
        file_name_index = file_name_number.zfill(4) + ".obj"
        # file_name_index = "%4d"% index + ".obj"
        os.rename(path + "\\" +file_name, path + "\\" +file_name_index)
        
        
        # f = open(path+"/"+file_name); #打开文件
        # iter_f = iter(f); #创建迭代器
        # str = ""
        # for line in iter_f: #遍历文件，一行行遍历，读取文本
        #     str = str + line
        # s.append(str) #每个文件的文本存到list中
# print(s) #打印结果