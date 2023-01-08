import torch

def knn_point(nsample, xyz, query_xyz):
    """
    Input:
        nsample: max sample number in local region
        xyz: all points, [B, N, C]
        query_xyz: query points, [B, S, C]
    Return:
        group_idx: grouped points index, [B, S, nsample]
    """
    sqrdists = square_distance(query_xyz, xyz)
    _, group_idx = torch.topk(sqrdists, nsample, dim = -1, largest=False, sorted=False)
    return group_idx

def square_distance(src, dst):
    """
    计算两组点集所有点, 两两之间的距离平方;
    Calculate Euclid distance between each two points.
    because: 
        dist = (xs - xd)^2 + (ys - yd)^2 + (zs - zd)^2
    and:
        src^T * dst = xs * xd + ys * yd + zs * zd;
        sum(src**2, dim=-1) = xs*xs + ys*ys + zs*zs;
        sum(dst**2, dim=-1) = xd*xd + yd*yd + zd*zd;
    therefore:
        dist = sum(src**2,dim=-1) + sum(dst**2,dim=-1) - 2*src^T*dst
    
    Input:
        src: source points, [B, N, C]
        dst: target points, [B, M, C]
    Output:
        dist: per-point square distance, [B, N, M]
    """
    B, N, C = src.shape
    _, M, _ = dst.shape
    
    src_cross_dst = -2 * torch.matmul(src, dst.permute(0, 2, 1))
    sum_src = torch.sum(src ** 2, -1).view(B, N, 1)
    sum_dst = torch.sum(dst ** 2, -1).view(B, 1, M) # NOTE: 一定要注意这里需要置换一下
    
    dist = src_cross_dst + sum_src + sum_dst 

    # 简易写法如下
    # dist += torch.sum(src ** 2, -1).view(B, N, 1)
    # dist += torch.sum(dst ** 2, -1).view(B, 1, M) # NOTE: 一定要注意这里需要置换一下
    return dist  # [src.num, dst.num]


def get_knn_index(coor_q, coor_k=None):
    coor_k = coor_k if coor_k is not None else coor_q
    # coor: bs, 3, np
    batch_size, _, num_points_q = coor_q.size()
    num_points_k = coor_k.size(2)

    with torch.no_grad():
#         _, idx = knn(coor_k, coor_q)  # bs k np
        idx = knn_point(5, coor_k.transpose(-1, -2).contiguous(), coor_q.transpose(-1, -2).contiguous()) # B G M
        idx = idx.transpose(-1, -2).contiguous()
        idx_base = torch.arange(0, batch_size, device=coor_q.device).view(-1, 1, 1) * num_points_k # 这里是为了区分不同 batch 的 k 近邻索引
        idx = idx + idx_base
        idx = idx.view(-1)
    
    return idx  # bs*k*np 


# for test
src = torch.randint(1, 10, [2,3,7])
dist = torch.randint(1, 10, [2,3,8])

res = get_knn_index(src, dist)


