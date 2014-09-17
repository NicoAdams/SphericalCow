import pygame
import math

class SampleSurface:
	def __init__(self):
		self.totalTime = 0
		self.points = []
		
	def draw(self, surface):
		surface.fill(pygame.Color(50,100,200))
		
		t = float(self.totalTime)
		x = 200 + 150*math.sin(t * .014983)
		y = 200 + 150*math.sin(t * .01) # * math.sin(t * .005)
		pygame.draw.polygon(surface, \
							pygame.Color(200,0,100), \
							((x, y), (x+50, y+100), (x+100, y)))
		
		point = (x+50, y+100)
		self.points += [point]
		for pnum in range(len(self.points)-1):
			p1 = self.points[pnum]
			p2 = self.points[pnum+1]
			pygame.draw.line(surface, pygame.Color(50,0,0), p1, p2)
		
	def update(self, time):
		self.totalTime += time
		
		