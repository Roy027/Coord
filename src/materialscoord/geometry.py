import numpy as np
from math import sqrt, floor

def round_decimals_down(number: float, decimals: int = 2):
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return floor(number)

    factor = 10 ** decimals
    return floor(number * factor) / factor

def coordinates_to_planes(xyz, threshold: float = 0.08715574274):
    """
    Return the distinct normal vector of planes given by the coordinates.
    
    Args:
        xyz: List of coordinates (site_name, (x, y, z))
        threshold: Minimum cross product magnitude to consider three points as a plane.
                  Default sin(5deg) approx 0.08715...
    """
    xyz_list = [i[1] for i in xyz]
    num = len(xyz_list)
    res = []
    
    # p1 is always the center atom (index 0)
    p1 = np.array(xyz_list[0])
    
    for j in range(1, num):
        for k in range(j + 1, num):
            p2 = np.array(xyz_list[j])
            p3 = np.array(xyz_list[k])
            
            v1 = p3 - p1
            v2 = p2 - p1
            
            # Normalize vectors
            v1_norm = np.linalg.norm(v1)
            v2_norm = np.linalg.norm(v2)
            
            if v1_norm == 0 or v2_norm == 0:
                continue
                
            n_v1 = v1 / v1_norm
            n_v2 = v2 / v2_norm
            
            vn = np.cross(n_v1, n_v2)
            vn_mag = np.linalg.norm(vn)
            
            if vn_mag >= threshold:
                res.append(vn)
    return res

def planes_to_dot_products(planes, decimals: int = 1):
    """
    Calculate dot products between normalized plane vectors.
    """
    num = len(planes)
    if num < 2:
        return []
        
    unit_planes = [plane / np.linalg.norm(plane) for plane in planes]
    dots = []
    
    for i in range(num - 1):
        for j in range(i + 1, num):
            dot = round_decimals_down(np.absolute(np.dot(unit_planes[i], unit_planes[j])), decimals)
            dots.append(dot)
    return dots
