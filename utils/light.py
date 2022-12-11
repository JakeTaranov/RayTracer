import numpy as np

class Light():
    def __init__(self, name, pos_x, pos_y, pos_z, l_r, l_g, l_b):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.pos = np.array([pos_x, pos_y, pos_z]).astype(float)
        self.c = [float(l_r), float(l_g), float(l_b)]
        
