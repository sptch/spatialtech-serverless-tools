import numpy as np 
import cv2

class Camera:

    def __init__(self,points):
        self.dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
        
        # hard coded image size
        self.size = (582.4, 1000, 3)
        
        self.focal_length = self.size[1]
        self.center = (self.size[1]/2, self.size[0]/2)
        self.camera_matrix = np.array(
                          [[self.focal_length, 0, self.center[0]],
                          [0, self.focal_length, self.center[1]],
                          [0, 0, 1]], dtype = "double"
                          )
        self.points = points

        

        self.image_points = []
        self.model_points = []

        for point in self.points:
            # 2D model points.
            x = point['point2d']['X']
            y = -point['point2d']['Y']
            s = list((x, y))
            self.image_points.append(s)
            # 3D model points.
            x = point['point3d']['X']
            y = point['point3d']['Y']
            z = point['point3d']['Z']
            s = list((x, y, z))
            self.model_points.append(s)

        self.image_points = np.asarray(self.image_points)
        self.model_points = np.asarray(self.model_points)


    
    def camera_position(self):
        _, rotation_vector, translation_vector, _ = cv2.solvePnPRansac(self.model_points, self.image_points, self.camera_matrix, self.dist_coeffs)
        rotM = cv2.Rodrigues(rotation_vector)[0]
        camera_position = -np.matrix(rotM).T*np.matrix(translation_vector)

        return camera_position, rotM