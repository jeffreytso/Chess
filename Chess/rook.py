import pygame
from piece import Piece
from errors import OutsideBoardError
"""Contains the rook class which is a subclass to the piece class."""

class Rook(Piece):
    """Can move horizontally and vertically for any number of squares."""
    def __init__(self, color, game_settings):
        """Calls the Piece superclass. has_moved is for castling."""
        super().__init__("rook", color, game_settings)
        self.has_moved = False

    def update(self):
        """Updates the rook's legal moves."""
        self.legal_moves = []
        x, y = self.rect.topleft
        direction = 0 
        # 0 = up, 1 = down, 2 = left, 3 = right
        while(direction <= 3):
            if direction == 0:
                y -= self.gs.SQUARE
            elif direction == 1:
                y += self.gs.SQUARE
            elif direction == 2:
                x -= self.gs.SQUARE
            elif direction == 3:
                x += self.gs.SQUARE

            try:
                piece = self.get_piece((x, y))
            except OutsideBoardError:
                x, y = self.rect.topleft
                direction += 1
                continue

            if piece == None:
                self.legal_moves.append((x, y))
            else:
                if piece.color != self.color:
                    self.legal_moves.append((x, y))
                x, y = self.rect.topleft
                direction += 1