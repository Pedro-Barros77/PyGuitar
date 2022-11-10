import pygame

from utils import math

BLACK = (0,0,0)
WHITE = (255,255,255)

GREEN_BTN = (56,171,55)
RED_BTN = (140,28,31)
YELLOW_BTN = (235, 203, 45)
BLUE_BTN = (13, 13, 222)
ORANGE_BTN = (204,117,38)

DARK_BROWN = (23, 17, 12)
GOLDEN_BROWN = (48, 43, 24)
GRAY = (135, 135, 135)
SILVER = (200, 203, 207)
CARBON = (31, 32, 33)
PURPLE = (98, 40, 173)

def add_evenly(color: tuple[int, int, int], weight: int):
    R_step = color[0] * weight // 255
    G_step = color[1] * weight // 255
    B_step = color[2] * weight // 255
    result = (
        math.clamp(color[0] + R_step, 0, 255), 
        math.clamp(color[1] + G_step, 0, 255), 
        math.clamp(color[2] + B_step, 0, 255)
        )
    return result

def add_alpha(color: tuple[int,int,int], value = 255):
    return (color[0], color[1], color[2], value)

def horizontal_gradient(size, startcolor, endcolor):
    """
    Draws a horizontal linear gradient filling the entire surface. Returns a
    surface filled with the gradient (numeric is only 2-3 times faster).
    """
    if(len(startcolor) == 3):
        startcolor = add_alpha(startcolor)
    if(len(endcolor) == 3):
        endcolor = add_alpha(endcolor)
        
    width = size[0]
    bigSurf = pygame.Surface((width, 1)).convert_alpha()
    dd = 1.0/width
    sr, sg, sb, sa = startcolor
    er, eg, eb, ea = endcolor
    rm = (er-sr)*dd
    gm = (eg-sg)*dd
    bm = (eb-sb)*dd
    am = (ea-sa)*dd
    for y in range(width):
        bigSurf.set_at((y,0),
                        (int(sr + rm*y),
                         int(sg + gm*y),
                         int(sb + bm*y),
                         int(sa + am*y))
                      )
    return pygame.transform.scale(bigSurf, size)