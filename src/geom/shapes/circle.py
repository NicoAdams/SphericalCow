from ..shape import Shape
from ..vector import Vector
from ..region import Region
import math

class Circle(Shape):
	"""Represents a circle object
	"""
	
	def __init__(self, center, radius, orientation=0):
		"""
		Arguments:
			center: [Vector] Circle's center
			radius: [float] Circle's radius
			orientation: [float] Circle's initial rotation (default: 0)
		"""
		self.center = center
		self.radius = radius
		self.orientation = orientation
	
	def __eq__(self, other):
		return self.center == other.center and self.radius == other.radius
	
	def __str__(self):
		return "Circle("+str(self.center)+", "+str(self.radius)+")"
	
	def type(self):
		return "circle"
	
	def legal(self):
		return radius > 0
	
	def copy(self):
		return Circle(self.center, self.radius)
	
	def equalsInRange(self, other, error):
		return self.center.equalsInRange(other.center, error) \
			and abs(self.radius - other.radius) < error
	
	def com(self):
		return self.center
	
	def move(self, change):
		self.center = self.center.add(change)
		return self
	
	def rotate(self, angle, about=None):
		if about is None: about = self.com()
		self.center = self.center.rotateAbout(angle, about)
		self.orientation += angle
		return self
	
	def area(self):
		return math.pi * math.pow(self.radius, 2)
	
	def area2(self, about=None):
		if about is None: about = self.com()
		val = math.pi * math.pow(self.radius, 4) / 2.
		# Perpendicular axis theorem
		val += self.area() * math.pow(self.center.sub(about).len(),2)
		return val
	
	def shadow(self, axis):
		if axis.len() == 0: return Region(0,0)
		
		axisCenter = self.center.project(axis)
		return Region(axisCenter.len() - self.radius, axisCenter.len() + self.radius)
		
	def segments(self, axis):
		return []
	
	def getCollisionAxes(self, other):
		return [self.center.sub(other.com())]
	
	def contains(self, point):
		return self.center.sub(point).len() < self.radius
	
	def intersections(self, other):
		# TODO
		pass
	