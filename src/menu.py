import pygame

class Menu:
	"""The opening game menu
	"""
		
	def __init__(self, color):
		self.color = color
	
	def draw(self, surface):
		"""Draws to the front-end surface
		"""
		bgColor = pygame.Color(100,200,200)
		surface.fill(self.color)
	
	def update(self, time):
		"""Updates internal logic
		"""
		