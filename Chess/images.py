import pygame
"""Classes that provide quality of life features for the game."""

class Image(pygame.sprite.Sprite):
    """A class for loading an image."""
    def __init__(self, image, alpha = 255, square = (0, 0)):
        """Loads an image with the specified transparency and location."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect()
        self.rect.topleft = square

class SquareBackground(Image):
    """A class for highlighting squares."""
    def __init__(self, square):
        """Loads a transparent background image for the specified square."""
        super().__init__("images/square_background.bmp", 0, square)
        

class GrayDot(Image):
    """A class for showing a pieces' legal moves."""
    def __init__(self, square):
        """Loads a semi-transparent dot for the specified square."""
        super().__init__("images/gray_dot.bmp", 128, square)

class Border(Image):
    """A class for showing a squares' border."""
    def __init__(self, square):
        """Loads a border around the specified square."""
        super().__init__("images/border.bmp", 0, square)
        self.image.set_colorkey((255, 255, 255))