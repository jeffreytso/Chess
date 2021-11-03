import pygame
from piece import Piece
from errors import OutsideBoardError
"""Contains the bishop class which is a subclass to the piece class."""

class Bishop(Piece):
    """Can move diagonally for any number of squares."""
    def __init__(self, color, game_settings):
        """Calls the Piece superclass."""
        super().__init__("bishop", color, game_settings)

    def update(self):
        """Updates the bishop's legal moves."""
        self.legal_moves = []
        x, y = self.rect.topleft
        direction = 0 
        # 0 = up-left, 1 = down-right, 2 = up-right, 3 = down-left
        while(direction <= 3):
            if direction == 0:
                y -= self.gs.SQUARE
                x -= self.gs.SQUARE
            elif direction == 1:
                y += self.gs.SQUARE
                x += self.gs.SQUARE
            elif direction == 2:
                y -= self.gs.SQUARE
                x += self.gs.SQUARE
            elif direction == 3:
                y += self.gs.SQUARE
                x -= self.gs.SQUARE

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