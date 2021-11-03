import pygame
"""Methods that have to do with being in check."""

def try_move_piece(piece, legal_moves, original_square, 
                            curr_square, game_settings):
    """Tries to move the piece to the current square."""
    captured_piece = piece.get_piece(curr_square)
    piece.rect.topleft = curr_square
    if captured_piece and captured_piece != piece:
        captured_piece.kill()
    game_settings.pieces.update()

    if not in_check(game_settings):
        legal_moves.append(curr_square)

    piece.rect.topleft = original_square
    if captured_piece:
        captured_piece.add(game_settings.pieces)
        if captured_piece.color == game_settings.p1.color:
            captured_piece.add(game_settings.p1.pieces)
        else:
            captured_piece.add(game_settings.p2.pieces)
    game_settings.pieces.update()


def in_check(game_settings):
    """Checks if you are in check."""
    color = game_settings.get_color()
    for piece in game_settings.pieces:
        if piece.color == color and piece.name == "king":
            king = piece
    for piece in game_settings.pieces:
        if (piece.color != color and
        king.rect.topleft in piece.legal_moves):
            return True
    return False

def update_in_check(game_settings):
    """Updates every pieces' legal moves with check into consideration."""
    # Contains a list of pairs of pieces and their legal moves.
    pairs = [] 
    for piece in game_settings.pieces:
        if piece.color == game_settings.get_color():
            legal_moves = []
            original_square = piece.rect.topleft
            for square in piece.legal_moves:
                try_move_piece(piece, legal_moves, 
                    original_square, square, game_settings)
            pairs.append((piece, legal_moves))
    for pair in pairs:
        pair[0].legal_moves = pair[1]
    for piece in game_settings.pieces:
        if piece.color != game_settings.get_color():
            piece.legal_moves = []

def game_over(game_settings):
    """Checks if game is over."""
    if game_settings.check_3_fold_rep():
        return "Three-Fold-Repetition"
    for piece in game_settings.pieces:
        if piece.color == game_settings.get_color() and piece.legal_moves:
            return False
    else:
        game_settings.pieces.update()
        if in_check(game_settings):
            return "Checkmate"
        else:
            return "Stalemate"