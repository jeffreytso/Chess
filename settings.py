import pygame, pawn as p, rook as r, horse as h
import bishop as b, king as k, queen as q
from player import Player
import images as img
from check import update_in_check
import sys
"""Contains the settings class."""

class Settings():
    """A class to store all settings for Chess."""
    def __init__(self):
        """Initializes the various settings for Chess."""

        # Size of a single square.
        self.SQUARE = 100

        # Creates a group to store all the pieces in play.
        self.pieces = pygame.sprite.Group()

        # Groups that stores images.
        self.dots = pygame.sprite.Group()
        self.square_backgrounds = pygame.sprite.Group()
        self.previous_move_bg = pygame.sprite.Group()
        self.borders = pygame.sprite.Group()

        # Keeps track of the currently selected piece.
        self.selected_piece = None

        # List of all positions ever reached.
        # A single position contains a tuple for every piece in play
        # that consists of the piece itself and its square.
        self.positions = []

        for x in range(0, self.SQUARE * 8, self.SQUARE):
            for y in range(0, self.SQUARE * 8, self.SQUARE):
                self.square_backgrounds.add(img.SquareBackground((x, y)))
                self.borders.add(img.Border((x, y)))

        # Player 1's color is on the bottom, player 2's color is on the top.
        # Sets the king and queen's x position depending on what color p1 is.
        self.p1 = Player("W")
        self.p2 = Player("B")

        if self.p1.color == "W":
            self.p1s_turn = True
        else:
            self.p1s_turn = False

    def draw_pieces(self):
        if self.p1.color == "W":
            p1_king_x = 4
            p2_king_x = 4
            p1_queen_x = 3
            p2_queen_x = 3
        else:
            p1_king_x = 3
            p2_king_x = 3
            p1_queen_x = 4
            p2_queen_x = 4

        for n in range(8):
            self.p1.pieces.add(p.Pawn(self.p1.color, self))
            self.p2.pieces.add(p.Pawn(self.p2.color, self))
        for n in range(2):
            self.p1.pieces.add(r.Rook(self.p1.color, self), 
                            h.Horse(self.p1.color, self), 
                            b.Bishop(self.p1.color, self))
            self.p2.pieces.add(r.Rook(self.p2.color, self), 
                            h.Horse(self.p2.color, self), 
                            b.Bishop(self.p2.color, self))
        self.p1.pieces.add(k.King(self.p1.color, self))
        self.p1.pieces.add(q.Queen(self.p1.color, self))
        self.p2.pieces.add(k.King(self.p2.color, self))
        self.p2.pieces.add(q.Queen(self.p2.color, self))
        self.pieces.add(self.p1.pieces, self.p2.pieces)

        # Creates a starting position for each piece 
        # type except for the king and queen.
        p1_p_start = 0
        p1_r_start = 0
        p1_h_start = self.SQUARE
        p1_b_start = self.SQUARE * 2
        p2_p_start = 0
        p2_r_start = 0
        p2_h_start = self.SQUARE
        p2_b_start = self.SQUARE * 2

        # Loops through each player's piece group and places them into
        # their correct square. Increments their horizontal position each
        # time so as not to create multiple pieces on the same square.
        for piece in self.p1.pieces:
            if piece.name == "pawn":
                piece.rect.topleft = (p1_p_start, self.SQUARE * 6)
                p1_p_start += self.SQUARE
            elif piece.name == "rook":
                piece.rect.topleft = (p1_r_start, self.SQUARE * 7)
                p1_r_start += self.SQUARE * 7
            elif piece.name == "horse":
                piece.rect.topleft = (p1_h_start, self.SQUARE * 7)
                p1_h_start += self.SQUARE * 5
            elif piece.name == "bishop":
                piece.rect.topleft = (p1_b_start, self.SQUARE * 7)
                p1_b_start += self.SQUARE * 3
            elif piece.name == "queen":
                piece.rect.topleft = (self.SQUARE * p1_queen_x, self.SQUARE * 7)
            elif piece.name == "king":
                piece.rect.topleft = (self.SQUARE * p1_king_x, self.SQUARE * 7)
        
        for piece in self.p2.pieces:
            if piece.name == "pawn":
                piece.rect.topleft = (p2_p_start, self.SQUARE)
                p2_p_start += self.SQUARE
            elif piece.name == "rook":
                piece.rect.topleft = (p2_r_start, 0)
                p2_r_start += self.SQUARE * 7
            elif piece.name == "horse":
                piece.rect.topleft = (p2_h_start, 0)
                p2_h_start += self.SQUARE * 5
            elif piece.name == "bishop":
                piece.rect.topleft = (p2_b_start, 0)
                p2_b_start += self.SQUARE * 3
            elif piece.name == "queen":
                piece.rect.topleft = (self.SQUARE * p2_queen_x, 0)
            elif piece.name == "king":
                piece.rect.topleft = (self.SQUARE * p2_king_x, 0)

    def update_every_move(self, original_square, curr_square):
        """Settings to update after every move."""
        self.square_backgrounds.add(self.previous_move_bg)
        self.previous_move_bg.empty()
        self.pieces.update()
        update_in_check(self)
        self.update_positions()
        self.dots.empty()
        for background in self.square_backgrounds:
            if (background.rect.topleft == original_square or
                     background.rect.topleft == curr_square):
                self.square_backgrounds.remove(background)
                self.previous_move_bg.add(background)
                background.image.set_alpha(255)
            else:
                background.image.set_alpha(0)
        self.selected_piece = None

    def get_color(self):
        """Gets the current player's color."""
        if self.p1s_turn:
            return self.p1.color
        else:
            return self.p2.color

    def draw_screen(self, board, screen):
        """Draws and displays the board, images, and pieces."""
        screen.blit(board, board.get_rect())
        self.dots.draw(screen)
        self.square_backgrounds.draw(screen)
        self.previous_move_bg.draw(screen)
        self.borders.draw(screen)
        self.pieces.draw(screen)
        pygame.display.flip()

    def update_positions(self):
        """Updates the list of positions."""
        position = []
        for piece in self.pieces:
            position.append((piece, piece.rect.topleft))
        self.positions.append(position)
        
    def check_3_fold_rep(self):
        """Checks for three-fold-repetition."""
        for position in self.positions:
            if self.positions.count(position) == 3:
                return True
        return False

    def game_over(self, game_result, screen):
        """Prompts the user to either play again or quit."""
        background = pygame.Surface((self.SQUARE * 4, self.SQUARE * 4))
        background.fill((0, 128, 0))
        play_again = img.Image("images/play_again.bmp")
        play_again.rect.center = (self.SQUARE * 4, self.SQUARE * 4.7)
        yes = img.Image("images/yes.bmp")
        yes.rect.center = (self.SQUARE * 3.5, self.SQUARE * 5.5)
        no = img.Image("images/no.bmp")
        no.rect.center = (self.SQUARE * 4.5, self.SQUARE * 5.5)

        IMG1_POS = (self.SQUARE * 4, self.SQUARE * 2.7)
        IMG2_POS = (self.SQUARE * 4, self.SQUARE * 3.7)

        if game_result == "Checkmate":
            img2 = img.Image("images/by_checkmate.bmp")
            if self.p1s_turn:
                img1 = img.Image("images/p2_wins.bmp")
            else:
                img1 = img.Image("images/p1_wins.bmp")
        else:
            img1 = img.Image("images/draw.bmp")
            if game_result == "Stalemate":
                img2 = img.Image("images/stalemate.bmp")
            else:
                img2 = img.Image("images/repetition.bmp")
        img1.rect.center = IMG1_POS
        img2.rect.center = IMG2_POS

        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_r:
                        game_over = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if yes.rect.collidepoint(event.pos):
                        game_over = False
                    elif no.rect.collidepoint(event.pos):
                        sys.exit()
            screen.blit(background, (self.SQUARE * 2, self.SQUARE * 2))
            screen.blit(img1.image, img1.rect)
            screen.blit(img2.image, img2.rect)
            screen.blit(play_again.image, play_again.rect)
            screen.blit(yes.image, yes.rect)
            screen.blit(no.image, no.rect)
            pygame.display.flip()