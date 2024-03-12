import pygame as pg
from pygame import Vector2
import numpy as np
import random
from copy import deepcopy

pg.init()

GAME_WIDTH, GAME_HEIGHT = 150, 100
SCALING = 7
SCREEN_WIDTH, SCREEN_HEIGHT = GAME_WIDTH*SCALING, GAME_HEIGHT*SCALING

SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def move_pixel_if_possible(x, y, new_x, new_y, pixel_id, grid):
    if 1 <= new_x < grid.width - 1 and 1 <= new_y < grid.height - 1:
        target_pixel = grid.intermediate_grid[new_x][new_y]
        if target_pixel != pixel_id:
            if target_pixel == 0:
                grid.intermediate_grid[new_x][new_y] = pixel_id
                grid.intermediate_grid[x][y] = 0
                return True
            if target_pixel == 2 or target_pixel == 5:
                if pixel_id == 1 or pixel_id == 3 or pixel_id == 6 or pixel_id == 4:
                    grid.intermediate_grid[new_x][new_y] = pixel_id
                    grid.intermediate_grid[x][y] = target_pixel
                    return True
            if target_pixel != 0:
                if (pixel_id == 3 or (pixel_id == 5 and new_y < y) or pixel_id == 11) and not (target_pixel == 3 or target_pixel == 5 or target_pixel == 11): #swap positions if fire, steam or smoke                        
                    grid.intermediate_grid[new_x][new_y] = pixel_id
                    grid.intermediate_grid[x][y] = target_pixel
                    return True
            if target_pixel == 3:
                if pixel_id == 2:
                    grid.intermediate_grid[new_x][new_y] = pixel_id
                    grid.intermediate_grid[x][y] = target_pixel
                    return True
    return False

class FallingBehavior:
    def update(self, pixel, x, y, grid):
        return move_pixel_if_possible(x, y, x, y + 1, pixel, grid)
    
class RisingBehavior:
    def update(self, pixel, x, y, grid):
        return move_pixel_if_possible(x, y, x, y - 1, pixel, grid)

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
                    move_pixel_if_possible(x, y, x + random.randrange(0, 2) * 2 - 1, y, pixel, grid)
                elif can_fall_right:                      
                    move_pixel_if_possible(x, y, x + 1, y + 1, pixel, grid)
                elif can_fall_left:                      
                    move_pixel_if_possible(x, y, x - 1, y + 1, pixel, grid)

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
                    move_pixel_if_possible(x, y, x + random.choice([-1, 1]), y, pixel, grid)
                elif can_move_left:
                    move_pixel_if_possible(x, y, x - 1, y, pixel, grid)
                elif can_move_right:
                    move_pixel_if_possible(x, y, x + 1, y, pixel, grid)

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
                move_pixel_if_possible(x, y, x + random.choice([-1, 1]), y, pixel, grid)
            elif can_move_left:
                move_pixel_if_possible(x, y, x - 1, y, pixel, grid)
            elif can_move_right:
                move_pixel_if_possible(x, y, x + 1, y, pixel, grid)

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
                                            
         

class DirtBehavior(SandBehavior):
    def update(self, pixel, x, y, grid):
        pass
      
class Grid:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.intermediate_grid = []
        self.pixels = [[0 for _ in range(self.height)] for _ in range(self.width)]

    def add_pixel(self, pixel_id, x, y):
        if (x > 0 and x < self.width and y > 0 and y < self.height):
            self.pixels[x][y] = pixel_id
            
    def update_pixels(self):
        self.pixels = deepcopy(self.pixels)
        self.intermediate_grid = deepcopy(self.pixels) 

        update_order = [(x, y) for x in range(1, self.width - 1) for y in range(1, self.height - 1)]
        random.shuffle(update_order)  # Randomize update order

        def check_around(x, y, target):
            
            if self.pixels[x][y + 1] == target and y + 1 < self.height - 1:
                return (x, y + 1)
            elif self.pixels[x][y - 1] == target and y - 1 > 1:
                return (x, y - 1)
            elif self.pixels[x + 1][y] == target and x + 1 < self.width - 1:
                return (x + 1, y)
            elif self.pixels[x - 1][y] == target and x - 1 > 1:
                return (x - 1, y)
            return None

        def move_pixel_if_possible(x, y, new_x, new_y, pixel_id):
            if 1 <= new_x < self.width - 1 and 1 <= new_y < self.height - 1:
                target_pixel = self.intermediate_grid[new_x][new_y]
                if target_pixel != pixel_id:
                    if target_pixel == 0:
                        self.intermediate_grid[new_x][new_y] = pixel_id
                        self.intermediate_grid[x][y] = 0
                        return True
                    if target_pixel == 2 or target_pixel == 5:
                        if pixel_id == 1 or pixel_id == 3 or pixel_id == 6 or pixel_id == 4:
                            self.intermediate_grid[new_x][new_y] = pixel_id
                            self.intermediate_grid[x][y] = target_pixel
                            return True
                    if target_pixel != 0:
                        if (pixel_id == 3 or (pixel_id == 5 and new_y < y) or pixel_id == 11) and not (target_pixel == 3 or target_pixel == 5 or target_pixel == 11): #swap positions if fire, steam or smoke                        
                            self.intermediate_grid[new_x][new_y] = pixel_id
                            self.intermediate_grid[x][y] = target_pixel
                            return True
            return False
        sand_pixel = SandBehavior()
        water_pixel = WaterBehavior()
        steam_pixel = SteamBehavior()
        behaviors = {
            1: SandBehavior(),
            2: WaterBehavior(),
            3: SteamBehavior()
        }
        for x, y in update_order:
            pixel = self.pixels[x][y] 
            if pixel != 0:
                if pixel == 1:   #sand
                    sand_pixel.update(pixel, x, y, self)
                    # if not move_pixel_if_possible(x, y, x, y + 1, pixel):
                
                    #     can_fall_right = False
                    #     can_fall_left = False

                    #     if y < self.height - 2:
                    #         if self.pixels[x + 1][y + 1] == 0 or self.pixels[x + 1][y + 1] == 2:
                    #             can_fall_right = True
                    #         if self.pixels[x - 1][y + 1] == 0 or self.pixels[x - 1][y + 1] == 2:
                    #             can_fall_left = True
                    #         if can_fall_left and can_fall_right:              
                    #             move_pixel_if_possible(x, y, x + random.randrange(0, 2) * 2 - 1, y, pixel)
                    #         elif can_fall_right:                      
                    #             move_pixel_if_possible(x, y, x + 1, y + 1, pixel)
                    #         elif can_fall_left:                      
                    #             move_pixel_if_possible(x, y, x - 1, y + 1, pixel)
                        
                elif pixel == 2: #water
                    water_pixel.update(pixel, x, y, self)
                    # became_dirt = False
                    # if not self.pixels[x][y + 1] == 1:
                    #     for i in range(10):
                    #         if y + i < self.height:
                    #             if self.pixels[x][y + i] == 1:
                    #                 if random.randrange(1, 2 + i * 100) < 10:
                    #                     self.intermediate_grid[x][y + i] = 6 #make dirt from sand under water
                    #                     self.intermediate_grid[x][y] = 0
                    #                     became_dirt = True
                    #                     break
                    # else:
                    #     self.intermediate_grid[x][y + 1] = 6 
                    # if not became_dirt:
                    #     should_evaporate = False
                  
                    #     if self.pixels[x][y - 1] == 0 and self.pixels[x][y + 1] != 0:
                    #         should_evaporate = (random.randrange(1, 100) == 1)
                    
                    #     if should_evaporate:
                            
                    #         self.intermediate_grid[x][y] = 3
                            
                    #     else:
                    
                    #         moved = False
                            
                    #         moved = move_pixel_if_possible(x, y, x, y + 1, pixel)
                    #         if not moved:
                    #             can_move_right = False
                    #             can_move_left = False
                    #             if y < self.height - 2:
                    #                 if self.pixels[x + 1][y] == 0 or self.pixels[x + 1][y] == 3:
                    #                     can_move_right = True
                    #                 if self.pixels[x - 1][y] == 0 or self.pixels[x - 1][y] == 3:
                    #                     can_move_left = True
                                        
                    #                 if can_move_right and can_move_left:
                    #                     move_pixel_if_possible(x, y, x + random.choice([-1, 1]), y, pixel)
                    #                 elif can_move_left:
                    #                     move_pixel_if_possible(x, y, x - 1, y, pixel)
                    #                 elif can_move_right:
                    #                     move_pixel_if_possible(x, y, x + 1, y, pixel)
                                                    
                elif pixel == 3: #steam
                    steam_pixel.update(pixel, x, y, self)
                    #if ((self.pixels[x][y - 1] != 0) or y < 1) and self.pixels[x][y + 1] == 0:
                    #     if random.randrange(1, 100) == 1:
                    #         self.intermediate_grid[x][y] = 2
                    # else:
                    #     if move_pixel_if_possible(x, y, x, y - 1, pixel):
                    #         y -= 1
                            
                    #     can_move_right = False
                    #     can_move_left = False
                    #     if y > 2:
                    #         if self.pixels[x + 1][y] == 0:
                    #             can_move_right = True
                    #         if self.pixels[x - 1][y] == 0:
                    #             can_move_left = True
                                
                    #         if can_move_right and can_move_left:
                    #             move_pixel_if_possible(x, y, x + random.choice([-1, 1]), y, pixel)
                    #         elif can_move_left:
                    #             move_pixel_if_possible(x, y, x - 1, y, pixel)
                    #         elif can_move_right:
                    #             move_pixel_if_possible(x, y, x + 1, y, pixel)
                        
                elif pixel == 4: #stone
                    
                    move_pixel_if_possible(x, y, x, y + 1, pixel)           
                
                elif pixel == 5: #lava
                    turned_to_stone = False
                    touching_water = check_around(x, y, 2)
                    if random.randrange(1, 100) == 1:
                        if self.pixels[x][y - 1] == 0:
                            self.intermediate_grid[x][y - 1] = 10
                    
                    if touching_water != None:
                        turned_to_stone = True
                        wx, wy = touching_water
                        self.intermediate_grid[wx][wy] = 3
                        self.intermediate_grid[x][y] = 4
                    
                    touching_grass = check_around(x, y, 7)
                    touching_wood = check_around(x, y, 8)
                    touching_leaves = check_around(x, y, 9)   
                    
                 

                    if touching_wood != None:
                        wx, wy = touching_wood
                        self.intermediate_grid[wx][wy] = 10
                    if touching_leaves != None:
                        wx, wy = touching_leaves
                        self.intermediate_grid[wx][wy] = 10
                    if touching_grass != None:
                        wx, wy = touching_grass
                        self.intermediate_grid[wx][wy] = 10
                    
                    if random.randrange(1, 300) == 1:
                        turned_to_stone = True
                    if turned_to_stone:
                        self.intermediate_grid[x][y] = 4

                    else:

                        
                        moved = move_pixel_if_possible(x, y, x, y + 1, pixel)
                        if not moved and y < self.height - 2:
                            can_move_right = False
                            can_move_left = False
                            if self.pixels[x + 1][y] == 0 or self.pixels[x + 1][y] == 3:
                                can_move_right = True
                            if self.pixels[x - 1][y] == 0 or self.pixels[x - 1][y] == 3:
                                can_move_left = True
                                
                            if can_move_right and can_move_left:
                                move_pixel_if_possible(x, y, x + random.choice([-1, 1]), y, pixel)
                            elif can_move_left:
                                move_pixel_if_possible(x, y, x - 1, y, pixel)
                            elif can_move_right:
                                move_pixel_if_possible(x, y, x + 1, y, pixel)
            
                elif pixel == 6: #dirt
                    
                    if not move_pixel_if_possible(x, y, x, y + 1, pixel):
                        can_fall_right = False
                        can_fall_left = False
                    
                        if y < self.height - 2:
                            if self.pixels[x + 1][y + 1] == 0 or self.pixels[x + 1][y + 1] == 2:
                                can_fall_right = True
                            if self.pixels[x - 1][y + 1] == 0 or self.pixels[x - 1][y + 1] == 2:
                                can_fall_left = True
                            if can_fall_left and can_fall_right:              
                                move_pixel_if_possible(x, y, x + random.randrange(0, 2) * 2 - 1, y, pixel)
                            elif can_fall_right:                      
                                move_pixel_if_possible(x, y, x + 1, y + 1, pixel)
                            elif can_fall_left:                      
                                move_pixel_if_possible(x, y, x - 1, y + 1, pixel)
                    can_spawn = True
                    for i in range(self.height - y - 1):
                        if self.pixels[x][y + i] == 0:
                            can_spawn = False 
                    if self.pixels[x][y - 1] != 0:
                        can_spawn = False
               
                    if random.randrange(1, 200) == 1 and can_spawn:
                        for i in range(random.randrange(1, 5)):
                            if y - i > 0:
                                if self.pixels[x][y - i - 1] == 0:
                                    self.intermediate_grid[x][y - i] = 7
                    elif random.randrange(1, 10000) == 1 and can_spawn:
                        leaves_width = 5
                        leaves_height = 25
                    
                        for i in range(leaves_width):
                            for j in range(leaves_height):
                                
                                x_coord = x - int(leaves_width/2) + i
                                y_coord = y - 10 - j
                                if x_coord > 0 and x_coord < self.width and y_coord > 0 and y_coord < self.height:
                                    if self.pixels[x_coord][y_coord] != 0 and self.pixels[x_coord][y_coord] != 7 and self.pixels[x_coord][y_coord] != 3 and self.pixels[x_coord][y_coord] != 2:
                                        can_spawn = False
                                        break
                
                        if can_spawn:   
                            for i in range(random.randrange(7, 20)):
                                if y - i > 0:
                                    if i > 10 and random.randrange(1, 5) == 1:
                                        branch_pos = random.choice([-1, 1])
                                        if self.pixels[x + branch_pos][y - i] == 0:
                                            self.intermediate_grid[x + branch_pos][y - i] = 8
                                    if i < 5 or self.pixels[x + 1][y] != 0 and self.pixels[x - 1][y] != 0:
                                        if self.pixels[x][y - i - 1] == 0 or self.pixels[x][y - i - 1] == 7:
                                            self.intermediate_grid[x][y - i] = 8
                                        else:
                                            break
                
                elif pixel == 7: #grass
                    if not move_pixel_if_possible(x, y, x, y + 1, pixel):
                        
                        if (self.pixels[x][y - 1] != 0 and self.pixels[x][y - 1] != 7 and random.randrange(1, 50) == 1) or self.pixels[x][y - 1] == 5:
                            self.intermediate_grid[x][y] = 6
                        elif y > self.height - 1 and self.pixels[x][y + 1] != 7 and self.pixels[x][y + 1] != 6:
                            self.intermediate_grid[x][y] = 0
                    pass
                
                elif pixel == 8: #wood
                    if not (self.pixels[x + 1][y] == 8 or self.pixels[x - 1][y] == 8):
                        move_pixel_if_possible(x, y, x, y + 1, pixel)
                    
                    if self.pixels[x][y - 1] == 0:
                        leaves_width = random.randrange(5, 13, 2)
                        leaves_height = random.randrange(5, 13, 2)

                        for i in range(leaves_width):
                            for j in range(leaves_height):
                                if not random.randrange(1, 50) == 1:
                                    if not ((i == 0 and j == 0) or (i == leaves_width - 1 and j == leaves_height - 1) or (i == leaves_width - 1 and j == 0) or (i == 0 and j == leaves_height - 1)):
                                        x_coord = x - int(leaves_width/2) + i
                                        y_coord = y - int(leaves_height/2) + j
                                    
                                        if x_coord > 0 and x_coord < self.width and y_coord > 0 and y_coord < self.height:
                                            if self.pixels[x_coord][y_coord] == 0:
                                                self.intermediate_grid[x_coord][y_coord] = 9
                                            
                elif pixel == 9: #leaves
                    # if (self.pixels[x + 1][y] == 9 or self.pixels[x + 1][y] == 8)  (self.pixels[x - 1][y] == 9 or self.pixels[x - 1][y] == 8):
                    #     move_pixel_if_possible(x, y, x, y + 1, pixel)
                    pass
                
                elif pixel == 10: #fire
                    if random.randrange(1, 10) == 1:
                        self.intermediate_grid[x][y] = 11
                    else:
                    
                            
                        touching_wood = check_around(x, y, 8)
                        touching_leaves = check_around(x, y, 9)

                        if touching_wood == None and touching_leaves == None:
                            if move_pixel_if_possible(x, y, x, y - 1, pixel):
                                y -= 1

                        elif random.randrange(1, 5) == 1:
                            if touching_wood != None:
                            
                                wx, wy = touching_wood
                                self.intermediate_grid[wx][wy] = 10
                            if touching_leaves != None:
                                wx, wy = touching_leaves
                                self.intermediate_grid[wx][wy] = 10
                    
                    
                        if y > 2:    
                            can_move_right = False
                            can_move_left = False
                            if self.pixels[x + 1][y] == 0:
                                can_move_right = True
                            if self.pixels[x - 1][y] == 0:
                                can_move_left = True
                                
                            if can_move_right and can_move_left:
                                move_pixel_if_possible(x, y, x + random.choice([-1, 1]), y, pixel)
                            elif can_move_left:
                                move_pixel_if_possible(x, y, x - 1, y, pixel)
                            elif can_move_right:
                                move_pixel_if_possible(x, y, x + 1, y, pixel)
                    
                elif pixel == 11: #smoke
                    if random.randrange(1, 50) == 1:
                        self.intermediate_grid[x][y] = 0
                    else:
                        if move_pixel_if_possible(x, y, x, y - 1, pixel):
                            y -= 1
                        if y > 2:
                            can_move_right = False
                            can_move_left = False
                            if self.pixels[x + 1][y] == 0:
                                can_move_right = True
                            if self.pixels[x - 1][y] == 0:
                                can_move_left = True
                                
                            if can_move_right and can_move_left:
                                move_pixel_if_possible(x, y, x + random.choice([-1, 1]), y, pixel)
                            elif can_move_left:
                                move_pixel_if_possible(x, y, x - 1, y, pixel)
                            elif can_move_right:
                                move_pixel_if_possible(x, y, x + 1, y, pixel)

                elif pixel == 12: #explosive
                    if not move_pixel_if_possible(x, y, x, y + 1, pixel):
                        touching_fire = check_around(x, y, 10)
                        touching_lava = check_around(x, y, 5)
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

                                    if new_pos_x < self.width and new_pos_x > 0 and new_pos_y < self.height and new_pos_y > 0:
                                        checked_pixel = self.pixels[new_pos_x][new_pos_y]
                                    
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

                                    if new_pos_x < self.width and new_pos_x > 0 and new_pos_y < self.height and new_pos_y > 0:
                                        checked_pixel = self.pixels[new_pos_x][new_pos_y]
                                        if checked_pixel != 4:
                                            if random.randrange(1, j + 2) == 1:
                                                self.intermediate_grid[new_pos_x][new_pos_y] = 10
                        
                                    else:
                                        break
                              
                                

        self.pixels = self.intermediate_grid

scale_factor = 1
active_grid = Grid(int(GAME_WIDTH/scale_factor), int(GAME_HEIGHT/scale_factor))

active_grid.add_pixel(0, 10, 10)

clock = pg.time.Clock()

def update(grid):
    #active_grid.update_pixel_positions()
    grid.update_pixels()

sand_noise = [[random.randrange(-10, 11) for _ in range(GAME_HEIGHT)] for _ in range(GAME_WIDTH)]

def render(grid):
    total_water = 0
    np_pixels = np.zeros((GAME_WIDTH, GAME_HEIGHT, 3), dtype=np.uint8)
    for x in range(grid.width):
        for y in range(grid.height):
            pixel = grid.pixels[x][y]
            dist_to_air = 1
            if pixel != 0 and pixel != 5:
                consecutive_air = 0
                for i in range(GAME_HEIGHT):
                    if (y - i > 0):
                        if grid.pixels[x][y - i] == 0 or grid.pixels[x][y - 1] == 5:
                            consecutive_air += 1
                            # dist_to_air = i / 3 + 1
                            # break
                        else:
                            consecutive_air = 0
                    else:
                        dist_to_air = i / 3 + 1
                        break
                    if consecutive_air > 5:
                        dist_to_air = i / 3 + 1
                        break
                    
            color = [50, 30, 0]
            if not (x == 0 or y == 0 or x == GAME_WIDTH - 1 or y == GAME_HEIGHT - 1):
                color = [25, 25, (155 - y) / 2]
                if pixel == 1:
                    color = [int(230 + sand_noise[x][y]) / dist_to_air, int((200 + sand_noise[x][y]) / dist_to_air), 0]
                elif pixel == 2:
                    total_water += 1
                    color = [0, int((122 + random.randrange(0, 20)) / (dist_to_air / 2)), int((232 + random.randrange(0, 10)) / (dist_to_air / 2))]
                elif pixel == 3:
                    total_water += 1
                    color = [int(170 / dist_to_air), int(222 / dist_to_air), int(220 / dist_to_air)]
                elif pixel == 4:
                    color = [int(150 / dist_to_air), int(150 / dist_to_air), int((150 + sand_noise[x][y]) / dist_to_air)]
                elif pixel == 5:
                    color = [155 + int(100 / dist_to_air), 50 + int((50 + random.randrange(1, 10) * 2) / dist_to_air), 0] 
                elif pixel == 6:
                    color = [int(150 / dist_to_air), int((100 + sand_noise[x][y] * 2) / dist_to_air), int(50 / dist_to_air)]
                elif pixel == 7:
                    color = [int(20 / dist_to_air), int((220 + sand_noise[x][y] * 2) / dist_to_air), int(50 / dist_to_air)]
                elif pixel == 8:
                    color = [int(200 / dist_to_air), int((150 + sand_noise[x][y]) / dist_to_air), int(50 / dist_to_air)]
                elif pixel == 9:
                    color = [int(20 / dist_to_air), int((220 + sand_noise[x][y] * 2) / dist_to_air), int(50 / dist_to_air)]
                elif pixel == 10:
                    color = [255, 70 + sand_noise[x][y] * 2, 10]
                elif pixel == 11:
                    color = [(10 + sand_noise[x][y]) / dist_to_air, (10 + sand_noise[x][y]) / dist_to_air, (10 + sand_noise[x][y]) / dist_to_air]
                elif pixel == 12:
                    color = [int(200 / dist_to_air), int((10 + sand_noise[x][y]) / dist_to_air), int(50 / dist_to_air)]
            color[0] *= 1.5
            color[1] *= 1.5
            color[2] *= 1.5
            
            
            if color[0] > 255:
                color[0] = 255
            if color[1] > 255:
                color[1] = 255
            if color[2] > 255:
                color[2] = 255
            color = (int(color[0]), int(color[1]), int(color[2]))
            np_pixels[x, y] = color

    initial_surface = pg.Surface((GAME_WIDTH, GAME_HEIGHT))
    pg.surfarray.blit_array(initial_surface, np_pixels)

    scaled_surface = pg.transform.scale(initial_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))

    SCREEN.blit(scaled_surface, (0, 0))
    
    pg.display.flip()

running = True
clicking = False

pixel_type = 1

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicking = True
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                pixel_type = 1
            elif event.key == pg.K_2:
                pixel_type = 2
            elif event.key == pg.K_3:
                pixel_type = 3
            elif event.key == pg.K_4:
                pixel_type = 4
            elif event.key == pg.K_5:
                pixel_type = 5
            elif event.key == pg.K_6:
                pixel_type = 6
            elif event.key == pg.K_q:
                pixel_type = 10
            elif event.key == pg.K_w:
                pixel_type = 12

    mouse_pos = pg.mouse.get_pos()
    for i in range(1):
        update(active_grid)
        if (clicking):
            brush_size = 5
        
            for x in range(brush_size):
                for y in range(brush_size):
                 
                    active_grid.add_pixel(pixel_type, x + int(mouse_pos[0] / SCALING), y + int(mouse_pos[1]/SCALING))
        update(active_grid)
    
    render(active_grid)
    #print("Water: ", active_grid.water_count)

    clock.tick(60)

pg.quit()
