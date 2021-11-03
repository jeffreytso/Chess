import pygame
import rook as r, horse as h, bishop as b, queen as q
from piece import Piece
from errors import OutsideBoardError
import sys
"""Contains the pawn class which is a subclass to the piece class."""

class Pawn(Piece):
    """
    Worth 1 point. 
    Can move upwards for one square.
    It's first move can be two squares.
    Can capture one square diagonally upwards.
    When the pawn reaches the last row, it 
    promotes to any other piece besides the king.
    """
    def __init__(self, color, game_settings):
        """
        Calls the Piece superclass. 
        moved_2_squares is for the pawn's first move.
        """
        super().__init__("pawn", color, game_settings)
        self.moved_2_squares = False

    def increment(self, y):
        """Changes the square depending on the piece's player."""
        # The pawn is the only piece that changes its rules with color.
        if self.color == self.gs.p1.color:
            y -= self.gs.SQUARE
        else:
            y += self.gs.SQUARE
        return y

    def update(self):
        """Updates the pawn's legal moves."""
        self.legal_moves = []
        squares_to_check = []
        x, y = self.rect.topleft

        if self.color == self.gs.p1.color:
            init_pawn_square = self.gs.SQUARE * 6
        else:
            init_pawn_square = self.gs.SQUARE

        y = self.increment(y)
        squares_to_check.extend(((x - self.gs.SQUARE, y), 
                                (x + self.gs.SQUARE, y), (x, y)))
        if self.rect.top == init_pawn_square:
            y = self.increment(y)
            squares_to_check.append((x, y))

        for square in squares_to_check:
            try:
                piece = self.get_piece(square)
            except OutsideBoardError:
                continue
            if square[0] == self.rect.left:
                if piece == None:
                    self.legal_moves.append(square)
                else:
                    break

            elif ((piece and piece.color != self.color) or 
            self.can_en_passant(square)):
                self.legal_moves.append(square)

    # --- Methods that relate to en passant ---
    def update_moved_2_squares(self, original_square, curr_square):
        """Updates whether the pawn has moved 2 squares."""
        for piece in self.gs.pieces:
            if piece.name == "pawn":
                if piece == self and abs(original_square[1] - curr_square[1]) > self.gs.SQUARE:
                    self.moved_2_squares = True
                else:
                    piece.moved_2_squares = False

    def can_en_passant(self, square):
        """Checks if the pawn can en_passant."""
        x, y = square
        if (self.rect.top == self.gs.SQUARE * 3 and 
        self.gs.p1.color == self.color):
            y = y + self.gs.SQUARE
        elif (self.rect.top == self.gs.SQUARE * 4 and 
        self.gs.p2.color == self.color):
            y = y - self.gs.SQUARE
        else:
            return
        piece_to_check = self.get_piece((x, y))
        if (piece_to_check and piece_to_check.name == "pawn" and 
        piece_to_check.moved_2_squares):
            return True
        else:
            return False


    # --- Methods that relate to promotion ---
    def can_promote(self):
        """Checks if you can promote."""
        return ((self.color == self.gs.p1.color and self.rect.top == 0) or 
        (self.color == self.gs.p2.color and self.rect.top == self.gs.SQUARE * 7))

    def draw_promote_choices(self, promotion_list, color):
        """Puts the promotion pieces in their correct spots to be drawn."""
        self.gs.dots.empty()
        for background in self.gs.square_backgrounds:
            background.image.set_alpha(0)
        x, y = self.rect.topleft
        for promotion_piece in promotion_list:
            promotion_piece.image.set_colorkey(None)
            promotion_piece.rect.topleft = (x, y)
            if color == self.gs.p1.color:
                y = y + self.gs.SQUARE
            else:
                y = y - self.gs.SQUARE

    def promote(self, promotion_piece):
        """Adds the promoted piece to it's correct groups."""
        promotion_piece.image.set_colorkey((253, 236, 166))
        promotion_piece.rect.topleft = self.rect.topleft
        promotion_piece.add(self.gs.pieces)
        if promotion_piece.color == self.gs.p1.color:
            promotion_piece.add(self.gs.p1.pieces)
        else:
            promotion_piece.add(self.gs.p2.pieces)

    def cancel_promotion(self, captured_piece, original_square):
        """Cancels the promotion and restarts the player's turn."""
        if captured_piece:
            captured_piece.add(self.gs.pieces)
            if captured_piece.color == self.gs.p1.color:
                captured_piece.add(self.gs.p1.pieces)
            else:
                captured_piece.add(self.gs.p2.pieces)
        self.add(self.gs.pieces)
        if self.color == self.gs.p1.color:
            self.add(self.gs.p1.pieces)
        else:
            self.add(self.gs.p2.pieces)
        self.gs.selected_piece = None
        self.rect.topleft = original_square

    def waiting_for_promotion(self):
        """Waits for the player to choose a piece or cancel the promotion."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                elif (event.type == pygame.MOUSEBUTTONDOWN and 
                event.button == 1):
                    return event.pos
                    running = False

    def promote_if_poss(self, board, screen):
        """Promotes if all the conditions are met."""
        promotion_list = pygame.sprite.Group([q.Queen(self.color, self.gs), 
                                            h.Horse(self.color, self.gs),
                                            r.Rook(self.color, self.gs),
                                            b.Bishop(self.color, self.gs)])
        if self.can_promote():
            self.kill()
            self.draw_promote_choices(promotion_list, self.color)
        else:
            return

        self.gs.draw_screen(board, screen)
        promotion_list.draw(screen)
        pygame.display.flip()

        square = self.waiting_for_promotion()

        for promotion_piece in promotion_list:
            if promotion_piece.rect.collidepoint(square):
                self.promote(promotion_piece)
                promotion_list.empty()
                promotion_list.draw(board)
                self.gs.draw_screen(board, screen)
                break
        else:
            promotion_list.empty()
            promotion_list.draw(board)
            self.gs.draw_screen(board, screen)
            return "Cancelled"