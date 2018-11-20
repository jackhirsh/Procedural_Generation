from __future__ import print_function

from general_functions import *
import numpy as np
import random
import math
import calendar
import time

class DiamondSquareGenerator():
    
    def __init__(self, seed, size, min_val, max_val, roughness):
        '''
        Constructor for the DiamondSquareGenerator class
        @param seed: The seed for the random generation
        @param size: The square size of the height map
        @param min_val: The minimum value of the height map
        @param max_val: The maximum value of the height map
        @param roughness: Value between 1 and 0 reflects the smoothness between cells
        '''
        # Adjust roughness into the acceptable range
        if roughness >= 1:
            roughness = 1
        elif roughness < 0:
            roughness = 0
        
        # Make sure the size is valid
        if (size - 1) % 2 != 0:
            raise Exception("Size Error: It must follow 'size = 2^n + 1'")
        
        # Seed the random number generator
        random.seed(seed)
        
        # Save the parameters
        self.size = size
        self.min_val = min_val
        self.max_val = max_val
        self.roughness = roughness
        
        # This is how many iterations of the two steps need to be made
        self.iters = int(math.log(self.size - 1, 2))
        
        # This is where the output map will be saved
        self.output = np.zeros((self.size, self.size))
        
        # Start the process of creating the final map
        self.init_corners()
        
        # Generate the map
        self.generate_map()
    
    def init_corners(self):
        '''
        Initializes the values of the corners to a random value in the given range
        '''
        self.output[0, 0] = random.uniform(self.min_val, self.max_val) # North West Corner
        self.output[0, self.size-1] = random.uniform(self.min_val, self.max_val) # North East Corner
        self.output[self.size-1, 0] = random.uniform(self.min_val, self.max_val) # South East Corner
        self.output[self.size-1,self.size-1] = random.uniform(self.min_val, self.max_val) # South West Corner
        print("Corners of the Diamond Square Map have been initialized")
    
    def generate_map(self):
        '''
        Generates the Diamond Square Map and saves it to self.output
        '''
        # Loop through completing however many iterations need to be made.
        # The number of sub divisions at each iteration gets multiplied by 4 at each step
        for i in range(1, self.iters + 2):
            # Calculate the distance between the center and the influences
            d = int(self.size // math.pow(2, i))
            # This means that it is finished
            if d == 0:
                break
            print("Starting Iteration: ", i, "/", (self.iters + 1))
            print("\t Point Distance: ", d)
            depth_modifier = 1 / (2*i) + .5
            
            # Calculate where all of the midpoints are for the diamond step
            midpoints = self.find_midpoint_locs(d)
                  
            # For every midpoint perform the diamond step
            for mpt in midpoints:
#                 print("Performing diamond step for point: ", mpt)
                self.diamond_step(mpt[1], mpt[0], d, depth_modifier)
#                 display_image("Debug", self.output)
            
            # Calculate where all of the points for the square step are
            sq_points = self.find_square_step_locs(midpoints, d)
            
            # For every point in sq_points calculate their values using the square step
            for spt in sq_points:
#                 print("Performing square step for point: ", spt)
                self.square_step(spt[1], spt[0], d, depth_modifier)
#                 display_image("Debug", self.output)
            
            
    def find_midpoint_locs(self, d):
        '''
        Calculates the locations of the midpoints used in the diamond step
        @param d: The distance in the horizontal/vertical between points
        @return: Returns a list of the midpoints
        '''
        midpoints = []
        rc = (self.size // (d*2))
        m_ct = int(math.pow(rc, 2))
        
        # For every row find all of the midpoints in that row
        start_point = [d, d] # The first point to find all of the others based off of
        midpoints.append(start_point)
        done = False
        
        # Iterate through the rest of the points
        for riter in range(0, rc):
            for citer in range(0, rc):
                # Skip the first point
                if riter == 0 and citer == 0:
                    continue
                point_row = d + (2*riter*d)
                point_col = d + (2*citer*d)
                point = [point_row, point_col]
                midpoints.append(point)
            
                
        print()    
        return midpoints
       
    def find_square_step_locs(self, midpoints, d):
        '''
        Finds the locations of the points to calculate during the square step
        @param midpoints: The midpoints used in the diamond step
        @param d: The distance in the horizontal/vertical between points
        @return: Returns the locations for the square step
        '''
        locs = []
        for mpt in midpoints:
            # Try to add a point to the left of the midpoint
            try:
                u_coord = mpt[1] - d
                loc = [mpt[0], u_coord]
                if loc not in locs:
                    locs.append(loc)
            except:
                print("Left edge out of the array skipping it")
            
            # Try to add a point to the right of the midpoint
            try:
                u_coord = mpt[1] + d
                loc = [mpt[0], u_coord]
                if loc not in locs:
                    locs.append(loc)
            except:
                print("Right edge out of the array skipping it")
                
            # Try to add a point to the top of the midpoint
            try:
                v_coord = mpt[0] + d
                loc = [v_coord, mpt[1]]
                if loc not in locs:
                    locs.append(loc)
            except:
                print("Top edge out of the array skipping it")
                
            # Try to add a point to the bottom of the midpoint
            try:
                v_coord = mpt[0] - d
                loc = [v_coord, mpt[1]]
                if loc not in locs:
                    locs.append(loc)
            except:
                print("Bottom edge out of the array skipping it")
        
        return locs   
                
    def diamond_step(self, u_cent, v_cent, d, depth_modifier):
        '''
        Performs the diamond step on the output map for the given point
        @param u_cent: The u coordinate of the center of the region to perform the step on
        @param v_cent: The v coordinate of the center of the region to perform the step on
        @param d: The horizontal/vertical point distance to the corners of the region
        @param depth_modifier: The depth into the map we are, the further down the less the adjacent values should vary (Smaller is further down)
        '''
        u_cent = int(u_cent)
        v_cent = int(v_cent)
        d = int(d)
        # Put all the points influencing the center point into a list
        influence = []
        influence.append(self.output[v_cent+d, u_cent+d]) # North East Corner
        influence.append(self.output[v_cent+d, u_cent-d]) # North West Corner
        influence.append(self.output[v_cent-d, u_cent+d]) # South East Corner
        influence.append(self.output[v_cent-d, u_cent-d]) # South West Corner
        
        # Calculate the value for the midpoint and set it in the output
        mag = (self.max_val * depth_modifier)
        value = (mean(influence)) + (random.uniform(-mag, mag))  # * self.roughness)) / 2
        self.output[v_cent, u_cent] = value
        
    def square_step(self, u_cent, v_cent, d, depth_modifier):
        '''
        Performs the square step on the output map for the given point
        @param u_cent: The u coordinate of the center of the region to perform the step on
        @param v_cent: The v coordinate of the center of the region to perform the step on
        @param d: The horizontal/vertical point distance to the edges of the region
        @param depth_modifier: The depth into the map we are, the further down the less the adjacent values should vary (Smaller is further down)
        '''
        u_cent = int(u_cent)
        v_cent = int(v_cent)
        d = int(d)
        # Try to add all of the edges of the square step to the influence list
        influence = []
        
        # Try to add the left edge
        if u_cent - d >= 0:
            influence.append(self.output[v_cent, u_cent-d])
            
        # Try to add the right edge
        if u_cent + d <= self.size - 1:
            influence.append(self.output[v_cent, u_cent+d])
            
        # Try to add the top edge
        if v_cent + d <= self.size - 1: 
            influence.append(self.output[v_cent+d, u_cent])
            
        # Try to add the bottom edge
        if v_cent - d >= 0:
            influence.append(self.output[v_cent-d, u_cent])
        
        mag = self.max_val * depth_modifier
        value = (mean(influence))+ (random.uniform(-mag, mag)) # * self.roughness)) / 2
        self.output[v_cent, u_cent] = value
        
        
if __name__ == '__main__':
    seed = random.random()
    dsg = DiamondSquareGenerator(seed, 127, 0, 255, .4)
    arr = dsg.output.astype(np.uint8)
    display_image("test", arr)
    import os
    save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images", str(calendar.timegm(time.gmtime()))) + ".png"
    cv2.imwrite(save_path ,arr)
        
        
        
        