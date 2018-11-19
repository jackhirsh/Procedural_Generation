from general_functions import *
import numpy as np
import random

class DoodleGenerator():
    
    def __init__(self, size, min_val, max_val):
        self._size = size
        self._min = min_val
        self._max = max_val
        self._map = np.zeros((size,size))
        
        # Require the map dimensions to be odd
        if (self._size - 1) % 2 != 0:
            raise Exception("The square size of the ds map needs to be of form 2^n + 1")
        
        # Generate the map
        self.generate_map()
        
    def generate_map(self):
        mpt = self._size // 2
        cur_u = mpt
        cur_v = mpt
        keep_going = True
        
        for v in range(self._size - 1):
            val = random.uniform(self._min, self._max)
            self._map[v][0] = val
        
        for u in range(1, self._size -1):
            self.compute_col(u)
    
    def compute_col(self, u):
        self._map[0][u] = random.uniform(self._min, self._max)
        for cur_v in range(1, self._size - 1):
            self.compute_value(u, cur_v)
    def compute_value(self, u, v):
        avg_these = []
        avg_these.append(self._map[v][u-1])
        avg_these.append(self._map[v][u+1])
        avg_these.append(self._map[v-1][u])
        avg_these.append(self._map[v+1][u-1])
        avg = mean(avg_these)
        val = (avg + random.uniform(self._min, self._max)) / 2
        
        self._map[v][u] = val
        
    def get_output(self):
        return self._map
    
if __name__ == '__main__':
    size = 17
    gen = DoodleGenerator(size, 0, 255)
    image = gen.get_output().astype(int)
    display_image("test", image)
    
    
    
    
    
    
    
    
    
    