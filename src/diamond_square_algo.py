from __future__ import print_function

import numpy as np
import random as random
import math
import cv2
from sklearn.preprocessing import normalize
from general_functions import *
    
class DiamondSquareMap():
    
    def __init__(self, size, range_min, range_max):
        '''
        Constructor for the DiamondSquareMap generator
        @param size: The square size of the map to generate
        @param range_min: Used in the magnitude computation
        @param range_max: Used in the magnitude computation
        '''
        self._size = size
        self._range_max = range_max
        self._range_min = range_min
        self._range_dif = self._range_max - self._range_min
        self._output = None
        
    def generate_map(self):
        '''
        Handles the full pipeline creation of the Diamond Square map
        Saves the final map in self._output
        '''
        # Make sure the size value is of the correct format
        if (self._size - 1) % 2 != 0:
            raise Exception("The square size of the ds map needs to be of form 2^n + 1")
        
        # Fill the output array with zeros for starters
        self._output = np.zeros((self._size, self._size))
        
        # Use range_dif as magnitude, this will be normalized later so it doesn't really matter
        self.generate_corners(self._range_dif)
        
        # Make the call to the recursive function calculate_map
        self._output = self.calculate_map(self._output, self._range_dif)
        
    def generate_corners(self, magnitude):
        '''
        Fills the corners of the output map with random values for use in the height map generation
        @param magnitude: The maximum magnitude of the random values
        '''
        self._output[0][0] = random.uniform(-magnitude, magnitude)
        self._output[0][self._size - 1] = random.uniform(-magnitude, magnitude)
        self._output[self._size - 1][0] = random.uniform(-magnitude, magnitude)
        self._output[self._size - 1][self._size - 1] = random.uniform(-magnitude, magnitude)
        
    def calculate_map(self, ds_map, magnitude):
        '''
        Calculates the values for the ds_map recursively
        @param ds_map: The ds_map to calculate the values for
        @param magnitude: The magnitude of the random value
        '''
        size = ds_map.shape[0]
        
        # Base case if the size of the map is just a single point
        if size == 1:
            return ds_map
        elif size == 3:
            ds_map = self.diamond_step(ds_map, magnitude)
            ds_map = self.square_step(ds_map, magnitude)
            return ds_map
        elif size == 2:
            print("something went wrong")
        # Main case that contains the recursive calls
        else:
            # Perform the diamond and square steps on the current map
            ds_map = self.diamond_step(ds_map, magnitude)
            ds_map = self.square_step(ds_map, magnitude)
            size = size
            sub_mag = magnitude * .56
            mid_point = (size // 2)
            
            
            # Recursive Calls
            # NW sub map
            ds_map[0:mid_point + 1, 0:mid_point + 1] = self.calculate_map(ds_map[0:mid_point + 1, 0:mid_point + 1], sub_mag)
            
            # SW sub map
            ds_map[mid_point:size, 0:mid_point + 1] = self.calculate_map(ds_map[mid_point:size, 0:mid_point + 1], sub_mag)
             
            # NE sub map
            ds_map[0:mid_point + 1, mid_point:size] = self.calculate_map(ds_map[0:mid_point + 1, mid_point:size], sub_mag)
             
            # SE sub map
            ds_map[mid_point:size, mid_point:size] = self.calculate_map(ds_map[mid_point:size, mid_point:size], sub_mag)
             
            return ds_map
        
    def diamond_step(self, ds_map, magnitude):
        '''
        Performs the diamond step on the given ds_map
        @param ds_map: The map to perform the step on
        @param magnitude: The magnitude of the random number to add
        @return: Returns the ds_map after the square step
        '''
        size = ds_map.shape[0]
        corner_vals = []
        corner_vals.append(ds_map[0][0])
        corner_vals.append(ds_map[0][size - 1])
        corner_vals.append(ds_map[size - 1][0])
        corner_vals.append(ds_map[size - 1][size - 1])
        
        mid_point = mean(corner_vals) + (random.uniform(-magnitude, magnitude))
        mid_coord = (size // 2)
        ds_map[mid_coord][mid_coord] = mid_point
        
        return ds_map
    
    def square_step(self, ds_map, magnitude):
        '''
        Completes the square step on the ds_map
        @param ds_map: The ds_map to perform the square step on
        @param magnitude: The max magnitude of the random value to add
        @return: Returns the ds_map after the square step
        '''
        size = ds_map.shape[0]
        
        corner_vals = []
        nw = ds_map[0][0] # NW
        ne = ds_map[0][size - 1] # NE
        sw = ds_map[size - 1][0] # SW
        se = ds_map[size - 1][size - 1] # SE
        
        mid_coord = (size // 2)
        mid = ds_map[mid_coord][mid_coord]
        
        # Left, Top, Bottom, Right
        # The coordinates to calculate at
        coords = [(mid_coord, 0), (0, mid_coord), (size - 1, mid_coord), (mid_coord, size - 1)]
        new_vals = [
            (nw + mid + sw) / 3 + (random.uniform(-magnitude, magnitude)),
            (nw + mid + ne) / 3 + (random.uniform(-magnitude, magnitude)),
            (sw + mid + se) / 3 + (random.uniform(-magnitude, magnitude)),
            (se + mid + ne) / 3 + (random.uniform(-magnitude, magnitude))]
        
        for iter, point in enumerate(coords):
            if ds_map[point[0]][point[1]] != 0:
                ds_map[point[0]][point[1]] = (ds_map[point[0]][point[1]] + new_vals[iter]) / 2
            else:
                ds_map[point[0]][point[1]] = new_vals[iter]
        
        return ds_map
    
    def get_output(self):
        '''
        Gets the unnormalized output array
        @return: Unnormalized output array
        '''
        if type(self._output) is None:
            self.generate_map()
        return self._output
    
    def get_normalized_color_value(self, intensity, min_limit, max_limit):
        '''
        Gets the color value normalized in the given range
        @param intensity: The intensity to interpret as a color value
        @param min_limit: The minimum value for the intensities
        @param max_limit: The maximum value for the intensities
        @return: Returns the color value for the given intensity
        '''
        min_max_difference = max_limit - min_limit
        intensity_cropped_by_max = np.where(intensity > max_limit, max_limit, intensity)
        intensity_cropped_by_min = np.where(intensity_cropped_by_max < min_limit, min_limit, intensity_cropped_by_max)
        intensity_cropped_zero_shifted = intensity_cropped_by_min - min_limit
        intensity_normalized = intensity_cropped_zero_shifted * 255 / min_max_difference
        return intensity_normalized.astype(np.uint8)
        
    def get_normalized(self, min_lim, max_lim):
        '''
        Gets the normalized output array
        @param min_lim: The minimum value of the normalized range
        @param max_lim: The maximum value of the normalized range
        @return: Returns the normalized array
        '''
        out = self.get_output()
        min = np.amin(out)
        max = np.amax(out)
        normalized = np.zeros_like(self._output, dtype=np.uint8)
        normalized[0:,0:] = self.get_normalized_color_value(self._output[0:,0:], min, max)
        return normalized
if __name__ == '__main__':
    sq_size = 129
    max_height = 255
    map_controller = DiamondSquareMap(sq_size, 0, max_height)
    map_controller.generate_map()
    map = map_controller.get_output()
    display_image("Unnormalized", map)
    norm = map_controller.get_normalized(0, 255)
    display_image("Normalized", norm)
    print(map_controller._output)
    print()
    