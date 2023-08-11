"""
Файл с настройками игры.
"""

import pygame as pg

# Настройка игры
TILE = 77
TILE_SUP = 231
ROW = 9
COL = 9
GAME_WINDOWS = ROW * TILE, COL * TILE + 100
FPS = 60

# Цвета
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BACKGROUND = (30, 30, 30)
GRID = (40, 40, 40)
GRAY = (105, 105, 105)

# Шрифты
pg.init()
FONT_NUMBER = pg.font.SysFont('timesnewroman', 40)
FONT_MAIN = pg.font.SysFont('Corbel', 40)
