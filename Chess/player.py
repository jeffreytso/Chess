import pygame

class Player():
	"""A class for creating the two players."""
	def __init__(self, color):
		"""Gives each player a piece color and group of pieces."""
		self.color = color
		self.pieces = pygame.sprite.Group()