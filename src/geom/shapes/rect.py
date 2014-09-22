from ..shape import Shape
from ..vector import Vector

class Rect(Shape):
	"""Represents a rectangular shape
	"""
	
	def __init__(self, x, y, width, height, angle):
		points = []
		points.append(Vector(x, y))
		points.append(Vector(x+width, y))
		points.append(Vector(x+width, y+height))
		points.append(Vector(x, y+height))
		
		self.points = points
		self.rotate(angle, about=Vector(x,y))
	