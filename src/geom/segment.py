import math
import numpy
from region import Region
from vector import Vector, fromPolar

class Segment(object):
	"""Represents a line segment from point to point
	Segment's domain is inclusive with respect to points
	"""
	
	def __init__(self, p1, p2):
		"""
		Arguments:
			p1, p2: [Vector] The line segment's boundaries
		"""
		self.p1 = p1
		self.p2 = p2
	
	def __eq__(self, other):
		return (self.p1 == other.p1 and self.p2 == other.p2) \
			or (self.p1 == other.p2 and self.p2 == other.p1)
	
	def __str__(self):
		return "Segment("+str(self.p1)+", "+str(self.p2)+")"
	
	def equalsInRange(self, other, error):
		return (self.p1.equalsInRange(other.p1, error) \
			and self.p2.equalsInRange(other.p2, error)) \
			or (self.p1.equalsInRange(other.p2, error) \
			and self.p2.equalsInRange(other.p1, error))
	
	def copy(self):
		return Segment(self.p1, self.p2)
	
	def len(self):
		return self.p1.sub(self.p2).len()
	
	def angle(self):
		return self.p1.sub(self.p2).angle()
	
	def center(self):
		return self.p1.add(self.p2).mul(.5)
	
	def translate(self, delta):
		"""Translates the segment by delta
		Arguments:
			delta: [Vector] The translation amount
		"""
		self.p1 = self.p1.add(delta)
		self.p2 = self.p2.add(delta)
		return self
	
	def rotate(self, angle, about=None):
		"""Rotates the segment
		Arguments:
			angle: [float] The rotation angle
			about: [Vector] The rotation center (default: origin)
		"""
		if about is None: about = Vector(0,0)
		self.p1 = self.p1.rotateAbout(angle, about)
		self.p2 = self.p2.rotateAbout(angle, about)
		return self
	
	def intersect(self, other, pThresh=0):
		"""Determines the intersection point of self and other
		Arguments:
			other: [Segment] A segment
			pThresh: [float] The permitted error when testing for parallel
				lines (default: 0) 
		Returns: [List [Vector]] Empty list for no intersect, one Vector for a
			point-intersect, two for a segment-intersect 
		"""
		
		# Manually handles zero-length lines
		if self.len() == 0 or other.len() == 0: return [] 
		
		# Manually handles point overlaps
		if self == other: return [self.p1, self.p2]
		if self.p1 == other.p1 or self.p1 == other.p2: return []
		if self.p2 == other.p1 or self.p2 == other.p2: return []
		
		# Maps problem to problem of locating other's x-intersect
		toTranslate = self.p1.mul(-1)
		toRotate = -1 * self.angle()
		s1 = self.copy()
		s2 = other.copy()
		s1.translate(toTranslate)
		s2.translate(toTranslate)
		s1.rotate(toRotate)
		s2.rotate(toRotate)
		
		# No x-intersect -- s2 does not cross s1's line
		if abs(s2.p1.y) > pThresh and numpy.sign(s2.p1.y) == numpy.sign(s2.p2.y):
			return []
		
		# Segments are parallel
		if abs(s2.p1.y) <= pThresh and abs(s2.p1.y) <= pThresh:
			s1region = Region(s1.p1.x, s1.p2.x)
			s2region = Region(s2.p1.x, s2.p2.x)
			overlap = s1region.overlapRegion(s2region)
			
			if overlap is False:
				# No intersection
				return []
			else:
				# Calculates segment of intersection
				p1Intersect = fromPolar(overlap.left, self.angle()) \
					.add(self.p1)
				p2Intersect = fromPolar(overlap.len(), self.angle()) \
					.add(p1Intersect)
				return [p1Intersect, p2Intersect]
		
		# Calculates the x-intersect
		xIntersect = s2.p1.x + (s2.p2.x - s2.p1.x) * (s2.p1.y / (s2.p1.y - s2.p2.y))
		
		if not Region(s1.p1.x, s1.p2.x).contains(xIntersect):
			# No x-intersect -- s2 crosses s1's line out of range of s1
			return []
		
		# Calculates and returns the intersection point
		pIntersect = fromPolar(xIntersect, self.angle()).add(self.p1)
		return [pIntersect]
	
	def overUnder(self, point, onThresh=0):
		"""
		Arguments:
			point: [Vector] A point
			onThresh: [float] The permitted error when testing for being "on" a line
		Returns: 1 if this point lies on or vertically over segment, -1 if
			lies vertically under, 0 if out of range over x
		"""
		
		rx = Region(self.p1.x, self.p2.x)
		ry = Region(self.p1.y, self.p2.y)
		
		if (not rx.contains(point.x)) or self.p1.x == self.p2.x:
			# Point is out of range over x
			return 0
		
		# y at the point where point is
		yThresh = self.p1.y + \
			(self.p2.y - self.p1.y) * \
			(point.x - self.p1.x) / (self.p2.x - self.p1.x)
		
		if abs(point.y - yThresh) < onThresh:
			# On segment
			return 1
		if point.y >= yThresh:
			# Over segment
			return 1
		else:
			# Under segment
			return -1
	
	