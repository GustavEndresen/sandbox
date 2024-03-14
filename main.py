import pygame as pg
from pygame import Vector2
import numpy as np
import random
from copy import deepcopy
from grid import Grid
pg.init()

GAME_WIDTH, GAME_HEIGHT = 150, 100
SCALING = 7
SCREEN_WIDTH, SCREEN_HEIGHT = GAME_WIDTH*SCALING, GAME_HEIGHT*SCALING

SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

scale_factor = 1
active_grid = Grid(int(GAME_WIDTH/scale_factor), int(GAME_HEIGHT/scale_factor))

active_grid.add_pixel(0, 10, 10)

clock = pg.time.Clock()

def update(grid):
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
                        dist_to_air = (i + 1) / 10 + 2
                        break
                    if consecutive_air > 10:
                        dist_to_air = (i + 1) / 10 + 2
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
                elif pixel == 13:
                    color = [255, 255, 0]
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
            elif event.key == pg.K_e:
                pixel_type = 13

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
