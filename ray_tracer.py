from utils.sceneparser import SceneParser
import sys
import numpy as np

EYE_ORIGIN = np.array([0,0,0])
BLACK = np.array([0,0,0])


class Ray:
    """
    Creates Ray Object (origin, direction, and a flag if it is a reflected ray)
    Provides functionality to assist with Ray Operations
    """
    def __init__(self, origin, direction, reflected_ray):
        self.origin = origin
        self.direction = direction
        self.is_reflected_ray = reflected_ray
        
    def point_at_intersection(self, root):
        return self.origin + self.direction * root
    
    def reflect(self, norm):
        return -2 * (np.dot(norm, self.direction)) * norm + self.direction
    
                
            
class Scene():
    """
    All rendering of the scene is done inside the "Scene" class
    """
    def __init__(self, spheres, lights, width, height, near, ambient, back):
        self.spheres = spheres
        self.lights = lights
        self.width = width
        self.height = height
        self.near = -near
        self.ambient = ambient
        self.bg_color = back
        self.max_depth = 3

        
    def render(self):
        """
        Main render loop for scene, loops over each pixel and call ray_trace which returns the final color of the pixel
        """
        pixels = [[None for _ in range(self.width)] for _ in range(self.height)]
        
        for c in range(self.height):
            for r in range(self.width):
                ray_dir = self.compute_ray_through_pixel(c, r)
                ray = Ray(EYE_ORIGIN, ray_dir, 0)
                color = self.ray_trace(ray, 0)
                pixels[c][r] = color
                
        return pixels
    
    def ray_trace(self, ray, depth):
        """
        Recursive ray trace function. Recurs max_depth times, responsible for gathering intersecions and colors. 
        """
        
        color = BLACK
        
        # After 3 reflections per ray, we exit
        if depth >= self.max_depth:
            return color
        
        # Find the closests Ray-Sphere interesection 
        intersection_with_sphere, s_c = self.get_closest_intersection(
            ray, ray.is_reflected_ray)
        
        
        # No collsion, so we return background color
        if intersection_with_sphere is None:
            # Return color (Black) if reflected ray does not collide with any other objects
            if ray.is_reflected_ray:
                return color
            # Else we return the color of the background
            return self.bg_color

        
        distance, sphere = intersection_with_sphere
        s, c = s_c
        intersection_point = ray.point_at_intersection(distance)


        canonical = Ray(s, c, 0)
        canonical_intersection = canonical.point_at_intersection(distance)

        sphere_surface_norm = self.get_sphere_normal(
            canonical_intersection, sphere)

        # Sums the Ambient, Diffuse, and Specular of the local area
        clocal = self.sum_shadow_rays(
            intersection_point, sphere_surface_norm, sphere)
        
        # Create the ray that is created after a reflection 
        reflected_ray = Ray(intersection_point, self.normalize(
            ray.reflect(sphere_surface_norm)), 1)
        # Recursive call on the reflected ray we calulcated
        color_reflected = self.ray_trace(reflected_ray, depth + 1)

        return clocal + color_reflected*sphere.k_r
    
    
    def sum_shadow_rays(self, intersection_point, sphere_surface_norm, sphere):
        """
        Calculates the local ambient, specular, and diffuse color. 
        Specular and diffuse are calucluated if and only if there is NOT a collision with nearby sphere (i.e it is in a shadow)
        """
        color = np.array([0.0,0.0,0.0])
        V = self.normalize(-intersection_point)
        
        #Ambient 
        for i in range(3):
            color[i] += self.ambient[i] * sphere.c[i] * sphere.k_a


        for light in self.lights:

            light_vec = self.normalize(light.pos - intersection_point)
            
            shadow_ray = Ray(intersection_point, light_vec, 0)
                        
            intersection, _ = self.get_closest_intersection(shadow_ray, shadow_ray.is_reflected_ray)

            light_dot_normal = max(np.dot(light_vec, sphere_surface_norm), 0)
            
            R = 2*np.dot(sphere_surface_norm, light_vec) * \
                sphere_surface_norm - light_vec
                
            ks = max(np.dot(R, V), 0.0)
            
            # if there is no intersection between the light source and the spot we are illuminating, then add diffuse and specular lighting
            if intersection is None:
                
                color = self.compute_diffuse_specular(color, sphere, light_dot_normal, light, ks)
                

        return color

    @staticmethod
    def compute_diffuse_specular(color, sphere, light_normal, light, ks):
        for i in range(3):
            #Diffuse
            color[i] += sphere.k_d*light.c[i] * \
                light_normal*sphere.c[i]
            # Specular
            color[i] += sphere.k_s*light.c[i] * \
                ks**sphere.n
                
        return color
    
    def get_sphere_normal(self, intersection_point, sphere):
        """
        Calculates and returns normal of sphere 
        """
        norm = self.normalize(
            np.dot(np.append(intersection_point, 0), np.transpose(sphere.m_inv)))

        return norm[:-1]
    
    
    

    def get_closest_intersection(self, ray, is_reflected):
        """
        Returns the point and sphere that the ray collides with, None if it doesnt collide
        """
        
        intersection = None
        s_c = None
        for sphere in self.spheres:

            # calculating the inverse of the sphere * ray origin 
            s = np.dot(sphere.m_inv, np.append(ray.origin, 1))[:-1]
            # calculating the inverse of the sphere * ray direction
            c = np.dot(np.append(ray.direction, 0), sphere.m_inv)[:-1]

            # with s and c, we solve a quadratic to see if there are any root (collisions)
            distance = self.solve_quadratic(s, c, is_reflected)

            if (distance is not None) and ((intersection is None) or (distance < intersection[0])):

                intersection = distance, sphere
                s_c = s, c

        return intersection, s_c
            
            
    def solve_quadratic(self, s, c, is_reflected):
        """
        Solves quadratic, returns the minimum (closest) of the t values computed.
        t represents the point at which there was an intersection.
        """
        mag_s = np.dot(s,s)
        mag_c = np.dot(c,c)
        
        a = mag_c
        b = np.dot(s,c)
        c = mag_s - 1
        
        desc = b**2 - (a*c)

        if desc >= 0:
            th_sub = -(b/a)-(np.sqrt(desc)/a) 
            th_add = -(b/a)+(np.sqrt(desc)/a) 
            
            min_val = min(th_sub, th_add)
                        
            
            if is_reflected and min_val > 0.0001:                
                return min_val
                
            if min_val >=1:
                return min_val

      
                
    def compute_ray_through_pixel(self, c, r):
        u_c = -1 + (2*r)/self.height
        v_r = -1 + (2*c)/self.width
        dir = self.normalize(np.array([u_c, v_r, self.near]))
        
        return dir
    
    @staticmethod
    def normalize(x):
        return x/np.linalg.norm(x)


def convert_color_and_scale(color):
    return "%s %s %s" % (str(int(min(color[0]*255, 255))), str(int(min(color[1]*255, 255))), str(int(min(color[2]*255, 255))))


        
def write_ppm_file(pixels):
    """
    Takes the rgb pixel colors we have calulated [0,1] and convertes it to a string "255,255,255" to write to the ppm file 
    """
    header = "P3 %s %s 255\n" % (len(pixels[0]), len(pixels))
    
    data_row = []
    for row in pixels[::-1]:
        cur_row = []
        for color in row:
            
            color = convert_color_and_scale(color)
            cur_row.append(color)
            
        data_row.append("   ".join(cur_row))
        
    return header + '\n'.join(data_row)
            

def main():
    if len(sys.argv) < 2:
        print("ERROR: missing test case file")
        sys.exit(1)

    test_file = str(sys.argv[1])
    scene_info = SceneParser(test_file)
    scene = Scene(scene_info.spheres, scene_info.lights, scene_info.width, scene_info.height, scene_info.near, scene_info.ambient, scene_info.back)
    
    pixels = scene.render()

    a = write_ppm_file(pixels)    
    
    with open(scene_info.output_file, "w") as raytraced_output:
        raytraced_output.write(a)

if __name__ == "__main__":
    main()