import pygame
from piece import Piece
from errors import OutsideBoardError
"""Contains the queen class which is a subclass to the piece class."""

class Queen(Piece):
    """Can move in all directions for any number of squares."""
    def __init__(self, color, game_settings):
        """Calls the Piece superclass."""
        super().__init__("queen", color, game_settings)

    def update(self):
        """Updates the queen's legal moves."""
        self.legal_moves = []
        x, y = self.rect.topleft
        direction = 0 
        # 0 = up, 1 = down, 2 = left, 3 = right 
        # 4 = up-left, 5 = down-right, 6 = up-right, 7 = down-left
        while(direction <= 7):
            if direction == 0:
                y -= self.gs.SQUARE
            elif direction == 1:
                y += self.gs.SQUARE
            elif direction == 2:
                x -= self.gs.SQUARE
            elif direction == 3:
                x += self.gs.SQUARE
            elif direction == 4:
                y -= self.gs.SQUARE
                x -= self.gs.SQUARE
            elif direction == 5:
                y += self.gs.SQUARE
                x += self.gs.SQUARE
            elif direction == 6:
                y -= self.gs.SQUARE
                x += self.gs.SQUARE
            elif direction == 7:
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