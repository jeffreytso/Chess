import pygame
from piece import Piece
from errors import OutsideBoardError
"""Contains the horse class which is a subclass to the piece class."""

class Horse(Piece):
    """Can move in an L-shape in all directions."""
    def __init__(self, color, game_settings):
        """Calls the Piece superclass."""
        super().__init__("horse", color, game_settings)

    def update(self):
        """Updates the horses' legal moves."""
        self.legal_moves = []
        square = self.gs.SQUARE
        squares_to_check = []
        x, y = self.rect.topleft
        squares_to_check.append((x + square * 2, y + square))
        squares_to_check.append((x + square, y + square * 2))
        squares_to_check.append((x - square * 2, y + square))
        squares_to_check.append((x - square, y + square * 2))
        squares_to_check.append((x - square * 2, y - square))
        squares_to_check.append((x - square, y - square * 2))
        squares_to_check.append((x + square * 2, y - square))
        squares_to_check.append((x + square, y - square * 2))

        for square in squares_to_check:
            try:
                piece = self.get_piece(square)
            except OutsideBoardError:
                continue

            if not piece or piece.color != self.color:
                self.legal_moves.append(square)