from pygame import Vector2
import random
import numpy as np

#level 1 superclasses
class FallingBehavior:
    def update(self, pixel, x, y, grid):
        return grid.move_pixel_if_possible(x, y, x, y + 1, pixel)
    
class RisingBehavior:
    def update(self, pixel, x, y, grid):
        return grid.move_pixel_if_possible(x, y, x, y - 1, pixel)

#level 2 superclasses
class SandBehavior(FallingBehavior):
    def update(self, pixel, x, y, grid):
        if not super().update(pixel, x, y, grid):
            can_fall_right = False
            can_fall_left = False
            if y < grid.height - 2:
                if grid.pixels[x + 1][y + 1] == 0 or grid.pixels[x + 1][y + 1] == 2:
                    can_fall_right = True
                if grid.pixels[x - 1][y + 1] == 0 or grid.pixels[x - 1][y + 1] == 2:
                    can_fall_left = True
                if can_fall_left and can_fall_right:              
                    grid.move_pixel_if_possible(x, y, x + random.randrange(0, 2) * 2 - 1, y, pixel)
                elif can_fall_right:                      
                    grid.move_pixel_if_possible(x, y, x + 1, y + 1, pixel)
                elif can_fall_left:                      
                    grid.move_pixel_if_possible(x, y, x - 1, y + 1, pixel)

class LiquidBehavior(FallingBehavior):
    def update(self, pixel, x, y, grid):
        if not super().update(pixel, x, y, grid):
            can_move_right = False
            can_move_left = False
            if y < grid.height - 2:
                if grid.pixels[x + 1][y] == 0 or grid.pixels[x + 1][y] == 3:
                    can_move_right = True
                if grid.pixels[x - 1][y] == 0 or grid.pixels[x - 1][y] == 3:
                    can_move_left = True
                    
                if can_move_right and can_move_left:
                    grid.move_pixel_if_possible(x, y, x + random.choice([-1, 1]), y, pixel)
                elif can_move_left:
                    grid.move_pixel_if_possible(x, y, x - 1, y, pixel)
                elif can_move_right:
                    grid.move_pixel_if_possible(x, y, x + 1, y, pixel)

class GasBehavior(RisingBehavior):
    def update(self, pixel, x, y, grid):
        if super().update(pixel, x, y, grid):
            y -= 1
            
        can_move_right = False
        can_move_left = False
        if y > 2:
            if grid.pixels[x + 1][y] == 0:
                can_move_right = True
            if grid.pixels[x - 1][y] == 0:
                can_move_left = True
                
            if can_move_right and can_move_left:
                grid.move_pixel_if_possible(x, y, x + random.choice([-1, 1]), y, pixel)
            elif can_move_left:
                grid.move_pixel_if_possible(x, y, x - 1, y, pixel)
            elif can_move_right:
                grid.move_pixel_if_possible(x, y, x + 1, y, pixel)
