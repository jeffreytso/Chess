class OutsideBoardError(Exception):
    """Raised when the specified square is outside the board."""
    pass

class OccupiedError(Exception):
    """Raised when the square specified is occupied with a piece the same color."""
    pass