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
            if y < grid.height - 1:
                if grid.pixels[x + 1][y] == 0 or grid.pixels[x + 1][y] == 3:
                    can_move_right = True
                if grid.pixels[x - 1][y] == 0 or grid.pixels[x - 1][y] == 3:
                    can_move_left = True
                    
                if can_move_right and can_move_left:
                    horizontal_depth = 10
                    right_count = 0
                    left_count = 0
                    for i in range(horizontal_depth):
                        if x + i < grid.width:
                            if grid.pixels[x + i][y] == pixel:
                                right_count += 1
                        if x - i > 0:
                            if grid.pixels[x - i][y] == pixel:
                                left_count += 1
                    move_dir = 0
                    if right_count > left_count:
                        move_dir = -1
                    elif left_count > right_count: 
                        move_dir = 1    
                    else:
                        move_dir = random.choice([-1, 1])
                    grid.move_pixel_if_possible(x, y, x + move_dir, y, pixel)
                elif can_move_left:
                    grid.move_pixel_if_possible(x, y, x - 1, y, pixel)
                elif can_move_right:
                    grid.move_pixel_if_possible(x, y, x + 1, y, pixel)


# class LiquidBehavior(FallingBehavior):
#     def update(self, pixel, x, y, grid):
#         # Use FallingBehavior's update first to attempt falling
#         if super().update(pixel, x, y, grid):
#             return True
        
#         # If falling is not possible, attempt to find the best flow path
#         flow_direction = self.find_best_flow_direction(x, y, grid)
#         if flow_direction:
#             nx, ny = x + flow_direction[0], y + flow_direction[1]
#             if self.is_valid_move(nx, ny, grid):
#                 return grid.move_pixel_if_possible(x, y, nx, ny, pixel)
#         return False

#     def find_best_flow_direction(self, x, y, grid):
#         directions = self.get_flow_directions(x, y, grid)
#         for d in directions:
#             nx, ny = x + d[0], y + d[1]
#             if self.is_valid_move(nx, ny, grid):
#                 return d
#         return None

#     def get_flow_directions(self, x, y, grid):
#         # Order matters: prioritize downward, then sideways, then diagonal
#         directions = [(0, 1), (-1, 0), (1, 0), (-1, 1), (1, 1)]
#         # Randomize sideways movement to prevent bias
#         random.shuffle(directions[1:3])
#         return directions

#     def is_valid_move(self, x, y, grid):
#         if 0 <= x < grid.width and 0 <= y < grid.height:
#             return grid.pixels[x][y] == 0  # Check if the spot is empty
#         return False







   

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

class FlammableBehavior():
    def update(self, pixel, x, y, grid):
        if grid.temperature > 30:
            if random.randrange(1, int((2000 / grid.temperature) * 100)) == 1:
                grid.intermediate_grid[x][y] = 14
                return True
        return False

class MeltableBehavior():
    def update(self, pixel, x, y, grid):
        if grid.temperature > 0:
            if random.randrange(1, int(500 / grid.temperature + 1)) == 1:
                grid.intermediate_grid[x][y] = 2
                return True
        return False
