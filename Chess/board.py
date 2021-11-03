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
    game_settings = Settings()
    screen = pygame.display.set_mode(
        (game_settings.SQUARE * 8, game_settings.SQUARE * 8))
    pygame.display.set_caption("Chess")
    board = pygame.image.load("images/board.bmp")

    # --- Starting screen ---
    start_screen = pygame.image.load("images/start_screen.bmp")
    x, y = (game_settings.SQUARE * 1.5, game_settings.SQUARE * 4.5)
    W_king = Image("images/Wking.bmp", 255, (x, y))
    x = x + game_settings.SQUARE * 2
    WB_king = Image("images/WBking.bmp", 255, (x, y))
    x = x + game_settings.SQUARE * 2
    B_king = Image("images/Bking.bmp", 255, (x, y))
    choices = pygame.sprite.Group(W_king, WB_king, B_king)
    for choice in choices:
        choice.image.set_colorkey((253, 236, 166))

    # --- Variables ---
    in_motion = False
    moving_piece = None
    running = True
    choosing_color = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)

        # --- Starting screen loop ---
        while choosing_color:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for choice in choices:
                        if choice.rect.collidepoint(event.pos):
                            game_settings = Settings()
                            if choice == W_king:
                                game_settings.p1.color = "W"
                                game_settings.p2.color = "B"
                                game_settings.p1s_turn = True
                            elif choice == B_king:
                                game_settings.p1.color = "B"
                                game_settings.p2.color = "W"
                                game_settings.p1s_turn = False
                            else:
                                if random.randint(1, 2) == 1:
                                    game_settings.p1.color = "W"
                                    game_settings.p2.color = "B"
                                    game_settings.p1s_turn = True
                                else:
                                    game_settings.p1.color = "B"
                                    game_settings.p2.color = "W"
                                    game_settings.p1s_turn = False
                            game_settings.draw_pieces()
                            game_settings.update_positions()
                            game_settings.pieces.update()
                            check.update_in_check(game_settings)
                            turn = game_settings.p1s_turn
                            choosing_color = False
            choices.draw(start_screen)
            screen.blit(start_screen, start_screen.get_rect())
            pygame.display.flip()

        for event in pygame.event.get():
            # --- Exiting and restarting the game ---
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_r:
                    choosing_color = True

            # --- Moving a piece ---
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                try:
                    original_square = game_settings.selected_piece.rect.topleft
                    curr_square = (int(event.pos[0] / 100) * 100, 
                                    int(event.pos[1] / 100) * 100)
                    game_settings.selected_piece.click_to_move(original_square,
                                                    curr_square, board, screen)
                except (AttributeError, OccupiedError):
                    for piece in game_settings.pieces:
                        if piece.rect.collidepoint(event.pos):
                            for border in game_settings.borders:
                                if border.rect.collidepoint(event.pos):
                                    border.image.set_alpha(255)
                            if game_settings.selected_piece != piece:
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
                for border in game_settings.borders:
                    border.image.set_alpha(0)

            elif event.type == pygame.MOUSEMOTION:
                if in_motion:
                    moving_piece.rect.center = event.pos
                    for border in game_settings.borders:
                        if border.rect.collidepoint(event.pos):
                            border.image.set_alpha(255)
                        else:
                            border.image.set_alpha(0)

        # Draws the board
        game_settings.draw_screen(board, screen)
        
        # Updates various settings after each turn
        if turn != game_settings.p1s_turn:
            game_settings.update_every_move(original_square, curr_square)
            game_result = check.game_over(game_settings)
            if game_result:
                game_settings.game_over(game_result, screen)
                choosing_color = True
        turn = game_settings.p1s_turn

run_game()