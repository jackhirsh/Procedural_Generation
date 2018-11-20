from general_functions import *
import numpy as np
import random

def perlin(mag, influence):
    return (mean(influence) + random.uniform(-mag//2, mag//2)) / 2
    
def generate2d(size, seed, mag):
    arr = np.zeros((size, size))
    for v in range(size):
        for u in range(size):
            if u == 0 and v == 0:
                arr[v][u] = seed
                arr[v+1][u] = seed
                arr[v][u+1] = seed
                arr[v+1][u+1] = seed
            else:
                influence = get_influence(arr, u, v)
                val = perlin(mag, influence)
                arr[v][u] = val
    return arr
                
def get_influence(arr, u, v):
    influence = []
    if u-1 >= 0:
        influence.append(arr[v][u-1])
    if u+1 <= arr.shape[0] - 1:
        influence.append(arr[v][u+1])
        
    if v-1 >= 0:
        influence.append(arr[v-1][u])
    if v+1 <= arr.shape[0] - 1:
        influence.append(arr[v+1][u])
        
    return influence

def get_normalized_color_value(intensity, min_limit, max_limit):
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
    
def get_normalized(arr, min_lim, max_lim):
    '''
    Gets the normalized output array
    @param min_lim: The minimum value of the normalized range
    @param max_lim: The maximum value of the normalized range
    @return: Returns the normalized array
    '''
    normalized = np.zeros_like(arr, dtype=np.uint8)
    normalized[0:,0:] = get_normalized_color_value(arr[0:,0:], min_lim, max_lim)
    return normalized
        
if __name__ == '__main__':
    arr = generate2d(1000, 100, 255)
    norm = get_normalized(arr, 0, 255)
    display_image("Test", arr)
    
    
    
    
    
    
    
    
    
    