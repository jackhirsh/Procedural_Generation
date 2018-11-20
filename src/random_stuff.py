from __future__ import print_function
from general_functions import *
import numpy as np
import cv2
import random

class TowerMaker():
    
    def __init__(self, sq_size, thick):
        self.sq_size = sq_size
        self.thick = thick
        self.image = np.full((sq_size,sq_size), 255, dtype=np.uint8)
        self.generate_tower(self.sq_size, self.thick)
        
    def generate_tower(self, sq_size, thick):
        start = (sq_size // 2) - (thick // 2)
        end = (sq_size // 2) + (thick // 2)
        self.image[0,start:end] = 0
        for row_num in range(1, sq_size):
            self.generate_layer(row_num)
            
    def generate_layer(self, row_num):
        for index in range(self.sq_size):
            random_num = int(random.uniform(1,10))
            secondary = int(random.uniform(1,100))
            main = random.uniform(1,10) * (index / self.thick) 
            print("row: ", row_num, "/", self.sq_size)
            if self.image[row_num - 1, index] == 0:
                if random_num != 10 and main >= 3:
                    self.image[row_num, index] = 0
            else:
                if random_num == 3 and secondary % 10 == 0 and secondary % 3 == 0:
                    self.image[row_num, index] = 0

if __name__ == '__main__':
    sq_size = 500
    thick = 5
    maker = TowerMaker(sq_size, thick)
    image = maker.image
    display_image("Test Image", image)