import numpy as np
import random
from copy import deepcopy
from pixel_behaviors import *

class Grid:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.intermediate_grid = []
        self.random_offsets_x = [random.randrange(-5, 5) for _ in range(self.width)]
        self.pixels = [[0 for _ in range(self.height)] for _ in range(self.width)]
        self.temperature = 25
    
    def check_around(self, x, y, target):
    
        if self.pixels[x][y + 1] == target and y + 1 < self.height - 1:
            return (x, y + 1)
        elif self.pixels[x][y - 1] == target and y - 1 > 1:
            return (x, y - 1)
        elif self.pixels[x + 1][y] == target and x + 1 < self.width - 1:
            return (x + 1, y)
        elif self.pixels[x - 1][y] == target and x - 1 > 1:
            return (x - 1, y)
        return None


    def move_pixel_if_possible(self, x, y, new_x, new_y, pixel_id):
        if 1 <= new_x < self.width - 1 and 1 <= new_y < self.height - 1:
            target_pixel = self.intermediate_grid[new_x][new_y]
       
            if target_pixel != pixel_id:
                if target_pixel == PT.ELECTRICITY.value or target_pixel == PT.HOTASH.value:
                    return False
                if target_pixel == PT.WOOD.value and new_x != x:
                    return False
                if target_pixel == PT.AIR.value:
                    self.intermediate_grid[new_x][new_y] = pixel_id
                    self.intermediate_grid[x][y] = 0
                    return True
                if target_pixel == 2 or target_pixel == PT.LAVA.value:
                    if pixel_id == PT.SAND.value or pixel_id == PT.STEAM.value or pixel_id == PT.DIRT.value or pixel_id == PT.STONE.value or pixel_id == PT.ICE.value or pixel_id == PT.HOTASH.value or pixel_id == PT.GRASS.value or pixel_id == PT.LEAVES.value:
                        self.intermediate_grid[new_x][new_y] = pixel_id
                        self.intermediate_grid[x][y] = target_pixel
                        return True
                if target_pixel != 0:
                    if (pixel_id == PT.STEAM.value or (pixel_id == PT.LAVA.value and new_y < y) or pixel_id == PT.SMOKE.value) and not (target_pixel == PT.STEAM.value or target_pixel == PT.LAVA.value or target_pixel == PT.SMOKE.value): #swap positions if fire, steam or smoke                        
                        self.intermediate_grid[new_x][new_y] = pixel_id
                        self.intermediate_grid[x][y] = target_pixel
                        return True
                if target_pixel == PT.STEAM.value:
                    if pixel_id == 2 or new_y > y:
                        self.intermediate_grid[new_x][new_y] = pixel_id
                        self.intermediate_grid[x][y] = target_pixel
                        return True
        return False

    def add_pixel(self, pixel_id, x, y):
        if (x > 0 and x < self.width and y > 0 and y < self.height):
            self.pixels[x][y] = pixel_id
            
    def update_pixels(self):
        self.pixels = deepcopy(self.pixels)
        self.intermediate_grid = deepcopy(self.pixels) 

        update_order = [(x, y) for x in range(1, self.width - 1) for y in range(1, self.height - 1)]
        random.shuffle(update_order)  # Randomize update order
        
        behaviors = [
            SandBehavior(),         #1
            WaterBehavior(),        #2
            SteamBehavior(),        #3
            StoneBehavior(),        #4
            LavaBehavior(),         #5
            DirtBehavior(),         #6
            GrassBehavior(),        #7
            WoodBehavior(),         #8
            LeafBehavior(),         #9
            FireBehavior(),         #10
            SmokeBehavior(),        #11
            DynamiteBehavior(),     #12
            ElectricityBehavior(),  #13
            FueledFireBehavior(),   #14
            HotAshBehavior(),       #15
            SnowBehavior(),         #16
            IceBehavior(),          #17
            AshBehavior(),
        ]

        for x, y in update_order:
            pixel = self.pixels[x][y] 
            if pixel > 0 and pixel <= len(behaviors): 
                behaviors[pixel - 1].update(pixel, x, y, self)     
                   

        self.pixels = self.intermediate_grid
