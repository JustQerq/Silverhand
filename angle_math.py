import numpy as np

def point2array(p):
  return np.array([p.x, p.y, p.z])

def equation_line(p1, p2):
    return (p2 - p1)

def equation_plane(p1, p2, p3):
    u = equation_line(p1, p2)
    v = equation_line(p1, p3)
    u_cross_v = np.cross(u, v)
    
    point = np.array(p1)
    normal = np.array(u_cross_v)
    
    D = -point.dot(normal)
    normal = np.floor_divide(normal, 10)
    return np.array([normal[0], normal[1], normal[2], D])

def angle_line_line(l1: np.ndarray, l2: np.ndarray):
  l1_mag = np.sqrt(l1.dot(l1))
  l2_mag = np.sqrt(l2.dot(l2))
  dot = l1.dot(l2)
  return np.degrees(np.arccos(dot/(l1_mag*l2_mag)))

def angle_line_plane(line, plane):
    line_np = line
    normal = plane[0:3]
    denominator = (np.sqrt(line_np.dot(line_np)) * np.sqrt(normal.dot(normal)))
    if(denominator == 0): return None
    return np.rad2deg(np.arcsin(abs(line_np.dot(normal)) / denominator))