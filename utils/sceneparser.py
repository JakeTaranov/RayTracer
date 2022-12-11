from utils.light import Light
from utils.sphere import Sphere
import numpy as np
import sys

class SceneParser():
    
    def __init__(self, test_file):
        self.test_file = test_file
        self.data = self.makeDataDict()
        self.near = int(self.data['NEAR'][0])
        self.left = int(self.data['LEFT'][0])
        self.right = int(self.data['RIGHT'][0])
        self.bottom = int(self.data['BOTTOM'][0])
        self.top = int(self.data['TOP'][0])
        self.width, self.height = int(
            self.data['RES'][0]), int(self.data['RES'][1])
        self.spheres = self.makeSpheres()
        self.lights = self.makeLights()
        self.back = np.array(self.data['BACK']).astype(float)
        self.ambient = np.array(self.data['AMBIENT']).astype(float)
        self.output_file = self.data['OUTPUT'][0]
        
        
        
    def makeLights(self):
        lights = []
        
        for light in self.data['LIGHTS']:
            name, pos_x, pos_y, pos_z, l_r, l_g, l_b = light[0], light[1], light[2], \
                light[3], light[4], light[5], \
                light[6]
            
            lights.append(Light(name, pos_x, pos_y, pos_z, l_r, l_g, l_b))

        return lights
        
    def makeSpheres(self):
        spheres = []
        for sphere in self.data["SPHERES"]:
            name, pos_x, pos_y, pos_z, scl_x, scl_y, scl_z, r, g, b, k_a, k_d, k_s, k_r, n = sphere[0], sphere[1], sphere[2],\
                sphere[3], sphere[4], sphere[5],\
                sphere[6], sphere[7], sphere[8],\
                sphere[9], sphere[10], sphere[11],\
                sphere[12], sphere[13], sphere[14],
                
            spheres.append((Sphere(name, pos_x, pos_y, pos_z, scl_x,
                         scl_y, scl_z, r, g, b, k_a, k_d, k_s, k_r, n)))
            
        return spheres
    
    def makeDataDict(self):
        
        data = {
            "SPHERES": [],
            "LIGHTS": []
        }
        try:
            with open(self.test_file) as file:
                for line in file:
                    stripped_split_line = line.rstrip().replace('\t', ' ').split(' ')
                    line = [s for s in stripped_split_line if s != '']
                    
                    if len(line) <= 1: continue
                    
                    data_type = line[0]
                    
                    if data_type == 'LIGHT' or data_type == "SPHERE":
                        data[data_type+'S'].append(line[1:])
                    else: 
                        data[data_type] = line[1:]
        except FileNotFoundError as e:
            print("Unable to open %s: %s" % (self.test_file, e))
            sys.exit(1)
            
        return data
            

    
    