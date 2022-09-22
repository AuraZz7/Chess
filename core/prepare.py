import pygame as pg
import os

from core import tools

# -------- SET UP SCREEN --------

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RLEACCEL)
pg.display.set_caption("Chess")

clock = pg.time.Clock()
fps = 60

# -------- COLOURS AND FONTS --------

board_col1 = (235, 236, 208)
board_col2 = (119, 149, 86)
yellow_1 = (246, 246, 105)
yellow_2 = (186, 202, 43)
circle_col1 = (214, 214, 189)
circle_col2 = (106, 135, 77)

# ---- GAME VARIABLES ----

rows = cols = 8
TILE_SIZE = T_S = SCREEN_WIDTH / rows

p = {
    "king": 0,
    "queen": 1,
    "b": 2,
    "k": 3,
    "r": 4,
    "p": 5
}

# -------- LOAD ASSETS --------

coordinates_w = ((0, 0), (333, 0), (666, 0), (1000, 0), (1333, 0), (1666, 0))
coordinates_b = ((0, 334), (333, 334), (666, 334), (1000, 334), (1333, 334), (1666, 334))
size = (333, 333)
d_s = (TILE_SIZE, TILE_SIZE)

p_white = tools.strip_coordinates_from_sheet(os.path.join("graphics", "chess_pieces.png"), coordinates_w, size, d_s)
p_black = tools.strip_coordinates_from_sheet(os.path.join("graphics", "chess_pieces.png"), coordinates_b, size, d_s)
