import pygame
import sys
from menu import Menu
from game import Game

from gameplay.geom.vector import Vector
print Vector

"""Initializes and runs the game
"""

pygame.init()

class Ticker:
	"""Tracks time ticks per update
	"""
	def __init__(self):
		self.prevTime = 0
	
	def tick(self):
		currTime = pygame.time.get_ticks()
		updateTime = currTime - self.prevTime
		self.prevTime = currTime
		return updateTime

ticker = Ticker()
clock = pygame.time.Clock()
fps = 30

# Opens window
windowSurface = pygame.display.set_mode((500,500))

# Defines some components
menu = Menu(pygame.Color(50,100,150))
game = Game()

# The currently active game component 
activeComponent = game

# Time of last update
prevTime = 0
updateTime = 0

# FPS
fps = 90

while True:	
	# Updates active component
	time = ticker.tick()
	activeComponent.update(time)
	
	# Draws screen
	activeComponent.draw(windowSurface)
	
	# Handles events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit() # Closes window
			sys.exit() # Exits program
		if event.type == pygame.MOUSEBUTTONDOWN:
			pass
	
	# Updates
	pygame.display.update() # Updates the display
	clock.tick(fps) # Pauses execution to fix fps
	