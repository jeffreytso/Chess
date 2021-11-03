import pygame
from errors import OutsideBoardError
from errors import OccupiedError
import check
from images import GrayDot
"""Conatins a class for piece sprites. Superclass to individual pieces."""

class Piece(pygame.sprite.Sprite):
    """A superclass to each of the piece sprites."""
    def __init__(self, name, color, game_settings):
        """Gives each piece a name, color, and list of legal moves."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/' 
                + color.upper() + name + '.bmp')
        self.image.set_colorkey((253, 236, 166))
        self.rect = self.image.get_rect()
        self.name = name
        self.color = color
        self.legal_moves = []
        self.gs = game_settings

    def get_piece(self, square):
        """Gets the piece on the specified square."""
        x, y = square
        if (x > self.gs.SQUARE * 7 or x < 0 or 
            y > self.gs.SQUARE * 7 or y < 0):
            raise OutsideBoardError
        for piece in self.gs.pieces:
            if square == piece.rect.topleft:
                return piece
        return None

    def snap_piece(self, original_square, curr_square, board, screen):
        """Snaps the piece to the correct square."""
        if curr_square in self.legal_moves:
            captured_piece = self.get_piece(curr_square)
            if captured_piece:
                captured_piece.kill()
            self.rect.topleft = curr_square

            # Castling
            if self.name == "king":
                self.castle_if_poss(original_square, curr_square)
                self.has_moved = True
            elif self.name == "rook":
                self.has_moved = True

            if self.name == "pawn":
                # Promotion
                if self.promote_if_poss(board, screen) == "Cancelled":
                    self.cancel_promotion(captured_piece, original_square)
                    return "promotion cancelled"

                # En passant
                if original_square[0] != curr_square[0]:
                    x, y = curr_square
                    if self.color == self.gs.p1.color:
                        y = y + self.gs.SQUARE
                    else:
                        y = y - self.gs.SQUARE
                    if self.get_piece((x, y)) and not captured_piece:
                        self.get_piece((x, y)).kill()
                self.update_moved_2_squares(original_square, curr_square)

            # End turn
            self.gs.p1s_turn = not self.gs.p1s_turn
        else:
            # Snap piece back to original square
            self.rect.topleft = original_square

    def click_to_move(self, original_square, curr_square, board, screen):
        """Calls snap_piece to move a piece without dragging."""
        original_square = self.rect.topleft
        is_occupied = self.get_piece(curr_square)
        promotion_cancelled = self.snap_piece(original_square, 
                                        curr_square, board, screen)
        if (original_square == self.rect.topleft and is_occupied and 
                                                not promotion_cancelled):
            raise OccupiedError
        self.gs.selected_piece = None
        self.gs.dots.empty()
        for background in self.gs.square_backgrounds:
            background.image.set_alpha(0)

    def toggle_legal_moves(self):
        """Shows and hides a pieces' legal moves."""
        self.gs.dots.empty()
        for background in self.gs.square_backgrounds:
            background.image.set_alpha(0)
        for background in self.gs.square_backgrounds:
            if background.rect.topleft == self.rect.topleft:
                if self == self.gs.selected_piece:
                    self.gs.selected_piece = None
                    background.image.set_alpha(0)
                else:
                    self.gs.selected_piece = self
                    for square in self.legal_moves:
                        dot = GrayDot(square)
                        self.gs.dots.add(dot)
                    background.image.set_alpha(128)