import pygame
"""Provides quality-of-life visuals for the game."""

class Visuals(pygame.sprite.Sprite):
    def loadImg(self, image, alpha = 255, square = (0, 0)):
        """Loads an image with the specified transparency and location."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect()
        self.rect.topleft = square

    def loadBackgroundSquare(self, square):
        """Loads a transparent background image for the specified square."""
        self.loadImg("images/square_background.bmp", 0, square)

    def loadGrayDot(self, square):
        """Loads a semi-transparent dot for the specified square."""
        self.loadImg("images/gray_dot.bmp", 128, square)

    def loadBorder(self, square):
        """Loads a border around the specified square."""
        self.loadImg("images/border.bmp", 0, square)
        self.image.set_colorkey((255, 255, 255))