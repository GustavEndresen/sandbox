from base_behaviors import *
from pygame import Vector2
import random
import numpy as np

#level 3 subclasses
class SteamBehavior(GasBehavior):
    def update(self, pixel, x, y, grid):
        if ((grid.pixels[x][y - 1] != 0) or y < 1) and grid.pixels[x][y + 1] == 0:
            if random.randrange(1, 100) == 1:
                grid.intermediate_grid[x][y] = 2
        else:
            super().update(pixel, x, y, grid)

class WaterBehavior(LiquidBehavior):
    def update(self, pixel, x, y, grid):
        became_dirt = False
        if not grid.pixels[x][y + 1] == 1:
            for i in range(10):
                if y + i < grid.height:
                    if grid.pixels[x][y + i] == 1:
                        if random.randrange(1, 2 + i * 100) < 10:
                            grid.intermediate_grid[x][y + i] = 6 #make dirt from sand under water
                            grid.intermediate_grid[x][y] = 0
                            became_dirt = True
                            break
        else:
            grid.intermediate_grid[x][y + 1] = 6 
        if not became_dirt:
            should_evaporate = False
        
            if grid.pixels[x][y - 1] == 0 and grid.pixels[x][y + 1] != 0:
                should_evaporate = (random.randrange(1, 100) == 1)
        
            if should_evaporate:
                
                grid.intermediate_grid[x][y] = 3
                
            else:
                super().update(pixel, x, y, grid)

class StoneBehavior(FallingBehavior):
    def update(self, pixel, x, y, grid):
        super().update(pixel, x, y, grid)    

class LavaBehavior(LiquidBehavior):
    def update(self, pixel, x, y, grid):
        turned_to_stone = False
        touching_water = grid.check_around(x, y, 2)
        if random.randrange(1, 100) == 1:
            if grid.pixels[x][y - 1] == 0:
                grid.intermediate_grid[x][y - 1] = 10
        
        if touching_water != None:
            turned_to_stone = True
            wx, wy = touching_water
            grid.intermediate_grid[wx][wy] = 3
            grid.intermediate_grid[x][y] = 4
        
        touching_grass = grid.check_around(x, y, 7)
        touching_wood = grid.check_around(x, y, 9)
        touching_leaves = grid.check_around(x, y, 9)   

        if touching_wood != None:
            wx, wy = touching_wood
            grid.intermediate_grid[wx][wy] = 10
        if touching_leaves != None:
            wx, wy = touching_leaves
            grid.intermediate_grid[wx][wy] = 10
        if touching_grass != None:
            wx, wy = touching_grass
            grid.intermediate_grid[wx][wy] = 10
        
        if random.randrange(1, 300) == 1:
            turned_to_stone = True
        if turned_to_stone:
            grid.intermediate_grid[x][y] = 4

        else:
            super().update(pixel, x, y, grid)
         
class DirtBehavior(SandBehavior):
    def update(self, pixel, x, y, grid):
        super().update(pixel, x, y, grid)
        can_spawn = True
        for i in range(grid.height - y - 1):
            if grid.pixels[x][y + i] == 0:
                can_spawn = False 
        if grid.pixels[x][y - 1] != 0:
            can_spawn = False
    
        if random.randrange(1, 200) == 1 and can_spawn:
            for i in range(random.randrange(1, 5)):
                if y - i > 0:
                    if grid.pixels[x][y - i - 1] == 0:
                        grid.intermediate_grid[x][y - i] = 7
                        pass
        elif random.randrange(1, 100) == 1 and can_spawn:
            leaves_width = 5
            leaves_height = 25
        
            for i in range(leaves_width):
                for j in range(leaves_height):
                    
                    x_coord = x - int(leaves_width/2) + i
                    y_coord = y - 5 - j
                    if x_coord > 0 and x_coord < grid.width and y_coord > 0 and y_coord < grid.height:
                        if grid.pixels[x_coord][y_coord] != 0 and grid.pixels[x_coord][y_coord] != 7 and grid.pixels[x_coord][y_coord] != 3 and grid.pixels[x_coord][y_coord] != 2:
                            can_spawn = False
                            break
    
            if can_spawn:   
                for i in range(random.randrange(7, 20)):
                    if grid.pixels[x][y - i] == 0:
                        grid.intermediate_grid[x][y - i] = 8
                        break
                    # if y - i > 0:
                    #     if i > 10 and random.randrange(1, 5) == 1:
                    #         branch_pos = random.choice([-1, 1])
                    #         if grid.pixels[x + branch_pos][y - i] == 0:
                    #             grid.intermediate_grid[x + branch_pos][y - i] = 8
                    #     if i < 5 or grid.pixels[x + 1][y] != 0 and grid.pixels[x - 1][y] != 0:
                    #         if grid.pixels[x][y - i - 1] == 0 or grid.pixels[x][y - i - 1] == 7:
                    #             grid.intermediate_grid[x][y - i] = 8
                    #         else:
                    #             break
         
class GrassBehavior(FallingBehavior):
    def update(self, pixel, x, y, grid):
        if not super().update(pixel, x, y, grid):
            if (grid.pixels[x][y - 1] != 0 and grid.pixels[x][y - 1] != 7 and random.randrange(1, 50) == 1) or grid.pixels[x][y - 1] == 5:
                grid.intermediate_grid[x][y] = 6
            elif y > grid.height - 1 and grid.pixels[x][y + 1] != 7 and grid.pixels[x][y + 1] != 6:
                grid.intermediate_grid[x][y] = 0

class WoodBehavior(FallingBehavior):
    def update(self, pixel, x, y, grid):
        
        if not (grid.pixels[x + 1][y] == 8 or grid.pixels[x - 1][y] == 8):
            super().update(pixel, x, y, grid)
        
        if grid.pixels[x][y - 1] == 0 and not grid.pixels[x - 1][y - 1] == 8 and not grid.pixels[x + 1][y - 1] == 8:
         
            height = 0
            for i in range(grid.height - y):
                if grid.pixels[x][y + i] == 8:
                    height += 1
                else:
                    break
            branch_side = random.choice([-1, 1])
            # if random.randrange(1, 10) == 1 and not grid.pixels[x + branch_side][y + 1] == 8:
            #     grid.intermediate_grid[x + branch_side][y] = 8
            
            if height < 15 + grid.random_offsets_x[x]:
                grid.intermediate_grid[x][y - 1] = 8
            else:
                
                leaves_width = random.randrange(5, 13, 2)
                leaves_height = random.randrange(5, 13, 2)

                for i in range(leaves_width):
                    for j in range(leaves_height):
                        if not random.randrange(1, 10) == 1:
                            if not ((i == 0 and j == 0) or (i == leaves_width - 1 and j == leaves_height - 1) or (i == leaves_width - 1 and j == 0) or (i == 0 and j == leaves_height - 1)):
                                x_coord = x - int(leaves_width/2) + i
                                y_coord = y - int(leaves_height/2) + j
                            
                                if x_coord > 0 and x_coord < grid.width - 1 and y_coord > 0 and y_coord < grid.height - 1:
                                    spawn_extra = random.randrange(1, 5) == 1
                              
                                    if spawn_extra:
                                        if i == 0:
                                            grid.intermediate_grid[x_coord - 1][y_coord] = 9
                                        if i == leaves_width - 1:
                                            grid.intermediate_grid[x_coord + 1][y_coord] = 9
                                    if grid.pixels[x_coord][y_coord] == 0:
                                        grid.intermediate_grid[x_coord][y_coord] = 9
                                        pass

class LeafBehavior():
    def update(self, pixel, x, y, grid):
        pass

class FireBehavior(GasBehavior):
    def update(self, pixel, x, y, grid):
        if random.randrange(1, 10) == 1:
            grid.intermediate_grid[x][y] = 11
        else:
            touching_wood = grid.check_around(x, y, 8)
            touching_leaves = grid.check_around(x, y, 9)

            if touching_wood == None and touching_leaves == None:
                if RisingBehavior().update(pixel, x, y, grid):
                    y -= 1

            elif random.randrange(1, 5) == 1:
                if touching_wood != None:
                
                    wx, wy = touching_wood
                    grid.intermediate_grid[wx][wy] = 10
                if touching_leaves != None:
                    wx, wy = touching_leaves
                    grid.intermediate_grid[wx][wy] = 10

            if y > 2: 
                super().update(pixel, x, y, grid)

class SmokeBehavior(GasBehavior):
    def update(self, pixel, x, y, grid):
        if random.randrange(1, 50) == 1:
            grid.intermediate_grid[x][y] = 0
        else:
            super().update(pixel, x, y, grid)

class DynamiteBehavior(FallingBehavior):
    def update(self, pixel, x, y, grid):
        if not super().update(pixel, x, y, grid):
            touching_fire = grid.check_around(x, y, 10)
            touching_lava = grid.check_around(x, y, 5)
            if touching_fire != None or touching_lava != None:
                #explode
                rays = 20
                total_force = 1000
                dead_rays = []
                for i in range(rays):
                    angle = i * (np.pi / rays * 2)
                    explosion_dir = Vector2(np.sin(angle), np.cos(angle))
                    for j in range(int(total_force / rays)):
                        new_pos_x = x + int(explosion_dir.x * j)
                        new_pos_y = y + int(explosion_dir.y * j)

                        if new_pos_x < grid.width and new_pos_x > 0 and new_pos_y < grid.height and new_pos_y > 0:
                            checked_pixel = grid.pixels[new_pos_x][new_pos_y]
                        
                            if checked_pixel == 4:
                                total_force += 50
                                dead_rays.append(i)
                                break
                        else:
                            break
                for i in range(rays):
                    if dead_rays.count(i) > 0:
                        continue
                    angle = i * (np.pi / rays * 2)
                    explosion_dir = Vector2(np.sin(angle), np.cos(angle))
                    for j in range(int(total_force / rays) + random.randrange(1, 10)):
                        new_pos_x = x + int(explosion_dir.x * j)
                        new_pos_y = y + int(explosion_dir.y * j)

                        if new_pos_x < grid.width and new_pos_x > 0 and new_pos_y < grid.height and new_pos_y > 0:
                            checked_pixel = grid.pixels[new_pos_x][new_pos_y]
                            if checked_pixel != 4:
                                if random.randrange(1, j + 2) == 1:
                                    grid.intermediate_grid[new_pos_x][new_pos_y] = 10
            
                        else:
                            break
