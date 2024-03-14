from base_behaviors import *
from pygame import Vector2
import random
import numpy as np

#level 3 subclasses
class SteamBehavior(GasBehavior):
    def update(self, pixel, x, y, grid):
        if ((grid.pixels[x][y - 1] != 0) or y < 1) and grid.pixels[x][y + 1] == 0 and random.randrange(1, 100) == 1:          
            grid.intermediate_grid[x][y] = 2
            return
            
        if grid.pixels[x][y + 1] == 0:
            if random.randrange(1, 10000) == 1:
                can_strike = True
                for i in range(grid.height - y):
                    if grid.pixels[x][y - 1] == 3:
                        continue
                    elif grid.pixels[x][y - 1] != 0:
                        
                        break
                    else:
                        can_strike = False
                        break
                if can_strike:
                    n_x = x
                    n_y = y
                    for i in range(100):
                        can_fall_left = False
                        can_fall_right = False
                        if grid.pixels[n_x + 1][n_y + 1] == 0:
                            can_fall_right = True
                        if grid.pixels[n_x - 1][n_y + 1] == 0:
                            can_fall_left = True
                        if can_fall_left and can_fall_right:              
                            n_x += random.choice([-1, 1])
                            n_y += 1
                        elif can_fall_right:                      
                            n_x += 1
                            n_y += 1
                        elif can_fall_left:                      
                            n_x -= 1
                            n_y += 1
                        if n_x < grid.width - 1 and n_y < grid.height - 1 and n_x > 0:   
                            grid.intermediate_grid[n_x][n_y] = 13
                        else:
                            break
                        if grid.pixels[n_x][n_y + 1] != 0 and grid.pixels[n_x][n_y + 1] != 3 and grid.pixels[n_x][n_y + 1] != 2 and grid.pixels[n_x][n_y + 1] != 13:
                            print(grid.pixels[n_x][n_y + 1])
                            for i in range(5):
                                grid.intermediate_grid[n_x + random.choice([-1, 1])][n_y + random.choice([-1, 1])] = 10
                            break
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
                    elif grid.pixels[x][y + i] == 15:
                        if random.randrange(1, 50) == 1:
                            grid.intermediate_grid[x][y + i] = 6 #make dirt from ash under water
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
            grid.intermediate_grid[wx][wy] = 14
        if touching_leaves != None:
            wx, wy = touching_leaves
            grid.intermediate_grid[wx][wy] = 14
        if touching_grass != None:
            wx, wy = touching_grass
            grid.intermediate_grid[wx][wy] = 14
        
        if random.randrange(1, 300) == 1:
            turned_to_stone = True
        if turned_to_stone:
            grid.intermediate_grid[x][y] = 4

        else:
            super().update(pixel, x, y, grid)
         
class DirtBehavior(SandBehavior):
    def update(self, pixel, x, y, grid):
        super().update(pixel, x, y, grid)
        can_spawn_grass = True
        can_spawn_tree = True
        for i in range(grid.height - y - 1):
            if grid.pixels[x][y + i] == 0:
                can_spawn_Tree = False
                can_spawn_grass = False
        if grid.pixels[x][y - 1] != 0:
            can_spawn_grass = False
            if grid.pixels[x][y - 1] != 7:
                can_spawn_tree = False
    
        if random.randrange(1, 10) == 1 and can_spawn_grass:
            for i in range(random.randrange(1, 5)):
                if y - i > 0:
                    if grid.pixels[x][y - i - 1] == 0:
                        grid.intermediate_grid[x][y - i] = 7
                        pass
        elif random.randrange(1, 1000) == 1 and can_spawn_tree:
            leaves_width = 10
            leaves_height = 25

            for i in range(leaves_width):
                for j in range(leaves_height):
                    
                    x_coord = x - int(leaves_width/2) + i
                    y_coord = y - 5 - j
                    if x_coord > 0 and x_coord < grid.width and y_coord > 0 and y_coord < grid.height:
                        if grid.pixels[x_coord][y_coord] != 0 and grid.pixels[x_coord][y_coord] != 7 and grid.pixels[x_coord][y_coord] != 3 and grid.pixels[x_coord][y_coord] != 2:
                            can_spawn_tree = False
                            break
    
            if can_spawn_tree:   
                for i in range(10):
                    if y - i > 0:
                        if grid.pixels[x][y - i] == 7 or grid.pixels[x][y - i] == 0:
                            grid.intermediate_grid[x][y - i] = 8
                            if grid.pixels[x][y - i] == 0:
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
            if random.randrange(1, 5) != 1:
                return
         
            height = 0
            can_grow = True
            for i in range(grid.height - y):
                if grid.pixels[x][y + i] == 8:
                    height += 1
                else:
                    if grid.pixels[x][y + i] != 6:
                        can_grow = False
                    break
            
            branch_side = random.choice([-1, 1])
            # if random.randrange(1, 10) == 1 and not grid.pixels[x + branch_side][y + 1] == 8:
            #     grid.intermediate_grid[x + branch_side][y] = 8
            
            if can_grow and height < 15 + grid.random_offsets_x[x]:
                grid.intermediate_grid[x][y - 1] = 8
                if random.randrange(1, 5) == 1:
                    grid.intermediate_grid[x + random.choice([-1, 1])][y] = 8
            
            elif height >= 15 + grid.random_offsets_x[x]:
                
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

class LeafBehavior(FallingBehavior):
    def update(self, pixel, x, y, grid):
        if grid.check_around(x, y, 9) == None:
            super().update(pixel, x, y, grid)
            
class FireBehavior(GasBehavior):
    def update(self, pixel, x, y, grid):
        if random.randrange(1, 10) == 1:
            grid.intermediate_grid[x][y] = 11
        else:
            touching_wood = grid.check_around(x, y, 8)
            touching_leaves = grid.check_around(x, y, 9)
            touching_grass = grid.check_around(x, y, 7)

            if touching_wood == None and touching_leaves == None and touching_grass == None:
                if RisingBehavior().update(pixel, x, y, grid):
                    y -= 1

            elif random.randrange(1, 2) == 1:
                if touching_wood != None:
                
                    wx, wy = touching_wood
                    grid.intermediate_grid[wx][wy] = 14
                if touching_leaves != None:
                    wx, wy = touching_leaves
                    grid.intermediate_grid[wx][wy] = 14
                if touching_grass != None:
                    wx, wy = touching_grass
                    grid.intermediate_grid[wx][wy] = 14

            if y > 2: 
                super().update(pixel, x, y, grid)

class FueledFireBehavior(GasBehavior):
    def update(self, pixel, x, y, grid):
        if random.randrange(1, 10) == 1:
            grid.intermediate_grid[x][y] = 15
        else:
            touching_wood = grid.check_around(x, y, 8)
            touching_leaves = grid.check_around(x, y, 9)

            if touching_wood == None and touching_leaves == None:
                grid.intermediate_grid[x][y] = 10
                return

            elif random.randrange(1, 6) == 1:
                if touching_wood != None:
                    wx, wy = touching_wood
                    grid.intermediate_grid[wx][wy] = 14
                if touching_leaves != None:
                    wx, wy = touching_leaves
                    grid.intermediate_grid[wx][wy] = 14

            if y > 2: 
                super().update(pixel, x, y, grid)

class AshBehavior(SandBehavior):
    def update(self, pixel, x, y, grid):
        
        touching_wood = grid.check_around(x, y, 8)
        touching_leaves = grid.check_around(x, y, 9)

        if random.randrange(1, 2) == 1:
            if touching_wood != None:
                wx, wy = touching_wood
                grid.intermediate_grid[wx][wy] = 14
            if touching_leaves != None:
                wx, wy = touching_leaves
                grid.intermediate_grid[wx][wy] = 14


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
                total_force = 500
                dead_rays = []
                for i in range(rays):
                    angle = i * (np.pi / rays * 2)
                    explosion_dir = Vector2(np.sin(angle), np.cos(angle))
                    for j in range(int(total_force / rays)):
                        new_pos_x = x + int(explosion_dir.x * j)
                        new_pos_y = y + int(explosion_dir.y * j)

                        if new_pos_x < grid.width and new_pos_x > 0 and new_pos_y < grid.height and new_pos_y > 0:
                            checked_pixel = grid.pixels[new_pos_x][new_pos_y]
                        
                            if checked_pixel == 4 or checked_pixel == 13:
                                total_force += j * 5
                    
                                break
                        else:
                            break
                for i in range(rays):
                   
                    angle = i * (np.pi / rays * 2)
                    explosion_dir = Vector2(np.sin(angle), np.cos(angle))
                    for j in range(int(total_force / rays) + random.randrange(1, 10)):
                        new_pos_x = x + int(explosion_dir.x * j)
                        new_pos_y = y + int(explosion_dir.y * j)

                        if new_pos_x < grid.width and new_pos_x > 0 and new_pos_y < grid.height and new_pos_y > 0:
                            checked_pixel = grid.pixels[new_pos_x][new_pos_y]
                            if checked_pixel != 4 and checked_pixel != 13:
                                if random.randrange(1, int(j / 4) + 2) == 1:
                                    grid.intermediate_grid[new_pos_x][new_pos_y] = 10
                            else:
                                break
            
                        else:
                            break

class ElectricityBehavior():
    def update(self, pixel, x, y, grid):
        grid.intermediate_grid[x][y] = 0