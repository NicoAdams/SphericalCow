from region import Region
from vector import Vector
from segment import Segment
import math
import numpy
from ..util import listEquals

class Shape(object):
	"""A polygon
	(Only valid for convex shapes)
	"""
	
	def __init__(self, points):
		"""
		Arguments:
			points: [List [Vector]] A list of points
		"""
		self.points = points
	
	def __eq__(self, other):
		return listEquals(self.points, other.points)
	
	def __str__(self):
		shapeStr = "Shape("
		for i in range(len(self.points)):
			p = self.points[i]
			if i > 0: shapeStr += ", "
			shapeStr += str(p)
		return shapeStr + ")"
	
	def type(self):
		return "polygon"
	
	def legal(self):
		# Returns true if shape is legal
		# TODO
		pass
	
	def copy(self):
		# Returns a copy of the shape
		return Shape(list(self.points))
	
	def equalsInRange(self, other, error):
		# Returns True if each point in other is equalInRange of each point in other
		if len(self.points) != len(other.points): return False
		for i in range(len(self.points)):
			p1 = self.points[i]
			p2 = other.points[i]
			if not p1.equalsInRange(p2, error):
				print "FALSE AT,", str(p1), str(p2)
				return False
		return True
	
	def com(self):
		# The center of mass
		comVal = Vector(0,0)
		for p in self.points:
			comVal = comVal.add(p)
		return comVal.mul(1.0 / len(self.points))
	
	def move(self, change):
		# Moves shape by the Vector change
		for i in range(len(self.points)):
			p = self.points[i]
			self.points[i] = p.add(change)
		return self
	
	def rotate(self, angle, about=None):
		"""Rotates the shape
		Arguments:
			angle: [float] Rotation angle
			about: [Vector] Rotation center (default: self.com())
		"""
		if about is None: about = self.com()
		for i in range(len(self.points)):
			p = self.points[i]
			self.points[i] = p.rotateAbout(angle, about)
		return self
	
	def area(self):
		# Returns the area of the shape
		areaVal = 0
		l = len(self.points)
		
		for i in range(l):
			p1 = self.points[i]
			p2 = self.points[(i+1) % l]
			w = p2.x - p1.x
			h = (p2.y + p1.y) / 2.0
			areaVal += w * h
		
		return abs(areaVal)
	
	def area2(self, about=None):
		"""
		Arguents:
			about: [Vector] Rotation center (default: self.com())
		Returns: [float] The moment of inertia about point "about"
		"""
		numer = 0
		denom = 0
		l = len(self.points)
		if about is None: about = self.com()
		
		for i in range(l):
			p1 = self.points[i]
			p2 = self.points[(i+1) % l]
			
			p1d = p1.sub(about)
			p2d = p2.sub(about)
			
			cross = float(p1d.scalarCross(p2d))
			numer += cross * (p1d.dot(p1d) + p1d.dot(p2d) + p2d.dot(p2d))
			denom += cross
		
		if denom == 0:
			return 0
		return float(numer) / denom
	
	def shadow(self, axis):
		"""
		Arguments:
			axis: [Vector] The axis onto which to project the shape
		Returns: [Region] representing the shape's "shadow" on axis
		"""
		lengths = []
		for p in self.points:
			lengths.append(p.project(axis).len())
		return Region(min(lengths), max(lengths))
		
	def segments(self):
		"""
		Returns: [List [Segment]] A list of segments in this shape
		"""
		segList = []
		l = len(self.points)
		for i in range(l):
			p1 = self.points[i]
			p2 = self.points[(i+1) % l]
			segList.append(Segment(p1, p2))
		return segList
	
	def getCollisionAxes(self, other):
		"""
		Arguments:
			other: [Shape] A Shape (for case where axis is collision-dependent)
		Returns: [List [Vector]] The possible axes of collision of other with self
		"""
		axes = []
		for s in self.segments():
			axes.append(s.p1.sub(s.p2).rotate(-math.pi/2).norm())
		return axes
	
	def mtv(self, other):
		"""
		Arguments:
			other: [Shape] A shape
		Returns: [Vector] The minimum translation vector of self with other
		"""
		axes = self.getCollisionAxes(other) + other.getCollisionAxes(self)
		
		mtvValue = float('infinity')
		mtvVector = Vector(0,0)
		for axis in axes:
			overlap = self.shadow(axis).minTranslation(other.shadow(axis))
			if(abs(overlap) < mtvValue):
				mtvValue = abs(overlap)
				mtvVector = axis.norm().mul(overlap)
		
		return mtvVector
	
	def contains(self, point):
		"""Determines whether a point is contained in a shape
		Should work on both convex and concave shapes
		Arguments:
			point: [Vector] A point
		Returns: [bool] True if this shape contains the point in it, else False
		"""
		
		"""Algorithm:
		Add up xDelta * overUnder for each segment in shape, where
		xDelta = 1 if segment goes L->R, -1 if R->L, 0 if vertical
		overUnder = 1 if point is over line, -1 if under, 0 if out of range
		If sum is nonzero, shape contains point
		"""
		pointState = 0
		for s in self.segments():
			xDelta = numpy.sign(s.p2.x - s.p1.x)
			overUnder = s.overUnder(point)
			pointState += xDelta * overUnder
			
		return pointState != 0
	
	def intersections(self, other, pThresh=0):
		"""Returns the set of intersections between self and other. When two
			lines intersect as a segment, returns the center of the 
			intersection segment
		Arguments:
			other: [Shape] The other shape
			pThresh: [float] The permitted error when testing for parallel
				lines (default: 0) 
		Returns: [List [Vector]] A list of the points of intersection between
			the shapes' sides
		"""
		# Lets other shapes handle more general intersection algorithms
		if not other.type() == self.type():
			return other.intersections(self)
			
		intersectList = []
		for s1 in self.segments():
			for s2 in other.segments():
				intersect = s1.intersect(s2, pThresh)
				if len(intersect) == 1:
					intersectList += intersect
				elif len(intersect) == 2:
					intersectList += \
						[Segment(intersect[0], intersect[1]).center()]
		return intersectList
	
	def getCollisionPoint(self, other, pThresh=0, p=False):
		"""Determines the "collision point" between two intersecting shapes
		Arguments:
			other: [Shape] The colliding shape
			pThresh: [float] The permitted error when testing for parallel
				lines (default: 0)
		Returns: [List [Vector]] An empty list if no collision, or a list of
			a single point if there is a collision
		"""
		intersectionList = self.intersections(other)
		if len(intersectionList) == 0:
			return []
		center = Shape(intersectionList).com()
		return [center]
	
