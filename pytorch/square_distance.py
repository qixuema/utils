def square_distance(src, dst):
    """
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
    B, N, _ = src.shape
    _, M, _ = dst.shape
    dist = -2 * torch.matmul(src, dst.permute(0, 2, 1))
    dist += torch.sum(src ** 2, -1).view(B, N, 1)
    dist += torch.sum(dst ** 2, -1).view(B, 1, M)
    return dist   