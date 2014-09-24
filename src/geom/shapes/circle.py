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
		if other.type() == "polygon":
			# Case 1: Polygon
			intersectList = []
			for segment in other.segments():
				c = self.copy()
				s = segment.copy()
				
				# Maps circle's center to origin, line to horizontal
				toMove = c.center.mul(-1)
				toRotate = -s.angle()
				c.move(toMove)
				s.move(toMove)
				s.rotate(toRotate, about=c.center)
				
				# Calculates intersects
				segmentHeight = s.p1.y
				segmentSpan = Region(s.p1.x, s.p2.x)
				segmentPoints = []
				if segmentHeight >= circle.radius:
					continue
				else:
					xMinPt = -math.sqrt(c.radius ** 2 - segmentHeight ** 2)
					xMaxPt =  math.sqrt(c.radius ** 2 - segmentHeight ** 2)
					if segmentSpan.contains(xMinPt):
						segmentPoints.append(Vector(xMinPt, segmentHeight))
					if segmentSpan.contains(xMaxPt):
						segmentPoints.append(Vector(xMaxPt, segmentHeight))
				
				# Translates solutions back to original coordinates
				for sp in segmentPoints:
					sp = sp.rotate(-toRotate, about=c.center)
					sp = sp.sub(toMove)
					intersectList.append(sp)
				
			return intersectList
			
			
		elif other.type() == "circle":
			# Case 2: Circle
			
			# Displacement
			d = other.center.sub(self.center).len()
			# Displacement angle
			dAngle = other.center.sub(self.center).angle()
			
			if d > other.radius + self.radius:
				# Circles are too far apart; no intersects
				return []
			elif d < abs(other.radius - self.radius):
				# One circle contains the other; no intersects
				return []
			else:
				# Aliases
				r1 = self.radius
				r2 = other.radius
				# Distance of intersect along displacement axis
				d1 = (d*d + r1*r1 - r2*r2) / (2*d)
				# Displacement of intersect perpendicularly from displacement axis
				y1 = (r1*r1 - d1*d1)
				
				# Intersections
				i1 = Vector(d1, y1)
				i2 = Vector(d1, y1)
				i1 = i1.add(self.center)
				i2 = i2.add(self.center)
				i1 = i1.rotate(dAngle)
				i2 = i2.rotate(dAngle)
				
				return [i1, i2]
		else:
			# Leaves it up to other shapes
			pass
		