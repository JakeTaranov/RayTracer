import numpy as np

class Sphere():
    def __init__(self, name, pos_x, pos_y, pos_z, scl_x, scl_y, scl_z, r, g, b, k_a, k_d, k_s, k_r, n):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.origin = np.array([pos_x, pos_y, pos_z])
        self.scl_x = scl_x
        self.scl_y = scl_y
        self.scl_z = scl_z
        self.r = r
        self.g = g
        self.b = b
        self.c = np.array([r,g,b]).astype(float)
        self.k_a = float(k_a)
        self.k_d = float(k_d)
        self.k_s = float(k_s)
        self.k_r = float(k_r)
        self.n = float(n)
        self.m_inv = np.linalg.inv(np.array([[self.scl_x, 0, 0, self.pos_x], 
                                             [0, self.scl_y, 0, self.pos_y], 
                                             [0, 0, self.scl_z, self.pos_z], 
                                             [0, 0, 0, 1]])
                                   .astype(float))
        
        

