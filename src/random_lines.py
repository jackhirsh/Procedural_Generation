import numpy as np
import cv2

class RandomPathGen():
    
    def __init__(self, size):
        self.size = size
        self.image = np.zeros((size,size))
        self.image[self.image == 0] = 255
        self.invalid_counter = 0
        
    def draw_line(self):
        last_direction = 0
        cv2.namedWindow("Test", cv2.WINDOW_NORMAL)
        for iter in range(self.size):
            nu, nv, last_direction = self.find_point(0, 0, last_direction)
            if last_direction == -1:
                break
            self.image[nv, nu] = 0
            cv2.imshow("Test", self.image)
            cv2.waitKey(1)
        pass
    
    def find_point(self, u, v, last_direction):
        nu, nv, new_direction = self.pick_next_point(u, v, last_direction)
        invalid_counter = 0
        while not(self.is_valid(nu, nv)):
            nu, nv, new_direction = self.pick_next_point(u, v, last_direction)
            if invalid_counter == 100:
                return -1, -1, -1
            
        return nu, nv, new_direction
    def pick_next_point(self, u, v, last_direction):
        
        new_direction = np.random.randint(0, 4)
        new_direction = (last_direction + new_direction) % 4
        
        nu = None
        nv = None
        
        if new_direction == 0:
            nu = u
            nv = v + 1
        elif new_direction == 1:
            nu = u + 1
            nv = v
        elif new_direction == 2:
            nu = u
            nv = v - 1
        elif new_direction == 3:
            nu = u - 1
            nv = v
        return nu, nv, new_direction
    
    
    def is_valid(self, nu, nv):
        if nv < 0 or nu < 0 or nv > self.size - 1 or nu > self.size - 1:
            return False
        if self.image[nv, nu] == 0:
            return False
        else:
            return True
        
        
        





if __name__ == '__main__':
    size = 50
    rpgen = RandomPathGen(size)
    rpgen.draw_line()
    cv2.namedWindow("Test", cv2.WINDOW_NORMAL)
    cv2.imshow("Test", rpgen.image)
    