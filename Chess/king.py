import pygame
from piece import Piece
from errors import OutsideBoardError
import check
"""Contains the king class which is a subclass to the piece class."""

class King(Piece):
    """Can move in all directions for one square."""
    def __init__(self, color, game_settings):
        """Calls the Piece superclass. has_moved is for castling."""
        super().__init__("king", color, game_settings)
        self.has_moved = False

    def update(self):
        """Updates the king's legal moves."""
        self.legal_moves = []
        squares_to_check = []
        x, y = self.rect.topleft
        for add_x in range(-self.gs.SQUARE, 
        self.gs.SQUARE * 2, self.gs.SQUARE):
            for add_y in range(-self.gs.SQUARE, 
            self.gs.SQUARE * 2, self.gs.SQUARE):
                if (add_x, add_y) == (0, 0):
                    continue
                squares_to_check.append((x + add_x, y + add_y))

        for square in squares_to_check:
            try:
                piece = self.get_piece(square)
            except OutsideBoardError:
                continue

            if not piece or piece.color != self.color:
                self.legal_moves.append(square)

        self.update_can_castle()

    def update_can_castle(self):
        """Adds castling into the king's list of legal moves if possible."""
        if not check.in_check(self.gs):
            for piece in self.gs.pieces:
                if (piece.color == self.color and piece.name == "rook" and 
                    (not (piece.has_moved or self.has_moved))):
                    rook = piece
                    orig_x, orig_y = self.rect.topleft
                    can_castle = True
                    castle_squares = []
                    if rook.rect.left > self.rect.left:
                        for x in range(orig_x + self.gs.SQUARE,
                                        rook.rect.left, self.gs.SQUARE):
                            castle_squares.append((x, orig_y))
                    else:
                        for x in range(rook.rect.left + self.gs.SQUARE,
                                        orig_x, self.gs.SQUARE):
                            castle_squares.append((x, orig_y))
                    for square in castle_squares:
                        for piece in self.gs.pieces:
                            if ((piece.color != self.color and 
                            (square in piece.legal_moves)) or 
                            piece.rect.collidepoint(square)):
                                can_castle = False
                    if can_castle:
                        if rook.rect.left > self.rect.left:
                            self.legal_moves.append((orig_x + 
                                                self.gs.SQUARE * 2, orig_y))
                        else:
                            self.legal_moves.append((orig_x - 
                                                self.gs.SQUARE * 2, orig_y))

    def castle_if_poss(self, original_square, curr_square):
        """Castles the king if conditions are met."""
        for piece in self.gs.pieces:
            if piece.color == self.color and piece.name == "rook":
                if self.move_is_castle(piece, original_square, curr_square):
                    piece.rect.left = (original_square[0] + curr_square[0]) / 2

    def move_is_castle(self, piece, original_square, curr_square):
        """Determines whether the move given is a castle."""
        return ((curr_square[0] - original_square[0]) > self.gs.SQUARE and 
                piece.rect.left == self.gs.SQUARE * 7 or 
                (original_square[0] - curr_square[0]) > self.gs.SQUARE and 
                piece.rect.left == 0)