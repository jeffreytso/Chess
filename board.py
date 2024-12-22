import pygame
import sys
from settings import Settings
import check
from errors import OccupiedError
from images import Image
import random

def run_game():
    """Runs the game."""
    pygame.init()
    gs = Settings()
    screen = pygame.display.set_mode(
        (gs.SQUARE * 8, gs.SQUARE * 8))
    pygame.display.set_caption("Chess")
    board = pygame.image.load("images/board.bmp")


    # --- Choosing Gamemode Screen ---
    choose_gamemode_screen = pygame.image.load("images/choose_gamemode_screen.bmp")
    x, y = (gs.SQUARE * 1.5, gs.SQUARE * 4.5)
    PvC = Image("images/PvC.bmp", 255, (x, y))
    x = x + gs.SQUARE * 2
    PvP = Image("images/PvP.bmp", 255, (x, y))
    x = x + gs.SQUARE * 2
    CvC = Image("images/CvC.bmp", 255, (x, y))
    gamemode_choices = pygame.sprite.Group(PvC, PvP, CvC)
    for gamemode_choice in gamemode_choices:
        gamemode_choice.image.set_colorkey((253, 236, 166))

    # --- Choosing Color Screen ---
    choose_color_screen = pygame.image.load("images/choose_color_screen.bmp")
    x, y = (gs.SQUARE * 1.5, gs.SQUARE * 4.5)
    W_king = Image("images/Wking.bmp", 255, (x, y))
    x = x + gs.SQUARE * 2
    WB_king = Image("images/WBking.bmp", 255, (x, y))
    x = x + gs.SQUARE * 2
    B_king = Image("images/Bking.bmp", 255, (x, y))
    color_choices = pygame.sprite.Group(W_king, WB_king, B_king)
    for color_choice in color_choices:
        color_choice.image.set_colorkey((253, 236, 166))

    # --- Variables ---
    in_motion = False
    moving_piece = None
    running = True
    choosing_gamemode = True
    choosing_color = True
    clock = pygame.time.Clock()

    runningPvP = False
    runningPvC = False
    runningCvC = False

    while running:
        clock.tick(60)

        # --- Choose between Player vs Player, Player vs Computer, and Computer vs Computer ---
        while choosing_gamemode:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for gamemode_choice in gamemode_choices:
                        if gamemode_choice.rect.collidepoint(event.pos):
                            if gamemode_choice == PvP:
                                runningPvP = True
                            elif gamemode_choice == PvC:
                                runningPvC = True
                            elif gamemode_choice == CvC:
                                runningCvC = True
                            choosing_gamemode = False
                            choosing_color = True
            gamemode_choices.draw(choose_gamemode_screen)
            screen.blit(choose_gamemode_screen, choose_gamemode_screen.get_rect())
            pygame.display.flip()

        # --- PvC Loop ---
        while runningPvC:
            continue


        # --- PvP Loop ---
        while runningPvP:
            # --- Starting screen loop ---
            while choosing_color:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for color_choice in color_choices:
                            if color_choice.rect.collidepoint(event.pos):
                                gs = Settings()
                                if color_choice == W_king:
                                    gs.p1.color = "W"
                                    gs.p2.color = "B"
                                    gs.p1s_turn = True
                                elif color_choice == B_king:
                                    gs.p1.color = "B"
                                    gs.p2.color = "W"
                                    gs.p1s_turn = False
                                else:
                                    if random.randint(1, 2) == 1:
                                        gs.p1.color = "W"
                                        gs.p2.color = "B"
                                        gs.p1s_turn = True
                                    else:
                                        gs.p1.color = "B"
                                        gs.p2.color = "W"
                                        gs.p1s_turn = False
                                gs.draw_pieces()
                                gs.update_positions()
                                gs.pieces.update()
                                check.update_in_check(gs)
                                turn = gs.p1s_turn
                                choosing_color = False
                color_choices.draw(choose_color_screen)
                screen.blit(choose_color_screen, choose_color_screen.get_rect())
                pygame.display.flip()

            for event in pygame.event.get():
                # --- Exiting and restarting the game ---
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_r:
                        runningPvP = False
                        choosing_gamemode = True

                # --- Moving a piece ---
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    try:
                        original_square = gs.selected_piece.rect.topleft
                        curr_square = (int(event.pos[0] / 100) * 100, 
                                        int(event.pos[1] / 100) * 100)
                        gs.selected_piece.click_to_move(original_square,
                                                        curr_square, board, screen)
                    except (AttributeError, OccupiedError):
                        for piece in gs.pieces:
                            if piece.rect.collidepoint(event.pos):
                                for border in gs.borders:
                                    if border.rect.collidepoint(event.pos):
                                        border.image.set_alpha(255)
                                if gs.selected_piece != piece:
                                    is_new_piece = True
                                    piece.toggle_legal_moves()
                                else:
                                    is_new_piece = False
                                original_square = piece.rect.topleft
                                in_motion = True
                                piece.rect.center = event.pos
                                moving_piece = piece
                                break

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        curr_square = (int(event.pos[0] / 100) * 100, 
                                        int(event.pos[1] / 100) * 100)
                        in_motion = False
                        if moving_piece:
                            moving_piece.snap_piece(original_square, 
                                                        curr_square, board, screen)
                            if original_square == curr_square:
                                if is_new_piece:
                                    is_new_piece = False
                                else:
                                    moving_piece.toggle_legal_moves()
                        moving_piece = None
                    for border in gs.borders:
                        border.image.set_alpha(0)

                elif event.type == pygame.MOUSEMOTION:
                    if in_motion:
                        moving_piece.rect.center = event.pos
                        for border in gs.borders:
                            if border.rect.collidepoint(event.pos):
                                border.image.set_alpha(255)
                            else:
                                border.image.set_alpha(0)

            # Draws the board
            gs.draw_screen(board, screen)
            
            # Updates various settings after each turn
            if turn != gs.p1s_turn:
                gs.update_every_move(original_square, curr_square)
                game_result = check.game_over(gs)
                if game_result:
                    gs.game_over(game_result, screen)
                    choosing_gamemode = True
                    runningPvP = False
            turn = gs.p1s_turn

run_game()