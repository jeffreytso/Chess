import pygame
import visuals as vs
import settings

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((100, 100)))
    pygame.display.set_caption("Chess")
    board = pygame.image.load("images/board.bmp")

    start_screen = pygame.image.load("images/start_screen.bmp")
    x, y = (settings.SQUARE * 1.5, settings.SQUARE * 4.5)
    W_king = vs.loadImg("images/Wking.bmp", 255, (x, y))
    x = x + settings.SQUARE * 2
    WB_king = vs.loadImg("images/WBking.bmp", 255, (x, y))
    x = x + settings.SQUARE * 2
    B_king = vs.loadImg("images/Bking.bmp", 255, (x, y))
    choices = pygame.sprite.Group(W_king, WB_king, B_king)
    for choice in choices:
        choice.image.set_colorkey((253, 236, 166))