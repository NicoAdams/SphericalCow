from segment import Segment
from shape import Shape
from region import Region
from vector import Vector
from shapes.circle import Circle
from shapes.rect import Rect
import math

"""Utility class for calculating shape intersections
Makes modding easier -- can see all current interactions
"""

class ShapePair:
	"""Stores two shapes for easier resolution of collision types
	"""
	def __init__(self, s1, s2, pThresh=0):
		"""
		Arguments:
			s1, s2: [Shape] Shapes
			pThresh: [float] The threshhold of error for considering two lines parallel
		"""
		self.shapes = (s1, s2)
		self.pThresh = 0
	
	def matches(self, type1, type2):
		"""
		Arguments:
			type1, type2: [str] Shape types
		Returns: True if s1 and s2's types match type1 and type2 in any order
		""" 
		return \
			(self.shapes[0].type() == type1 and self.shapes[1].type() == type2) or \
			(self.shapes[0].type() == type2 and self.shapes[1].type() == type1)
	
	def order(self, type1):
		"""Orders shape pair so that shapes[0] has type1
		"""
		if self.shapes[1].type() == type1:
			self.shapes = (self.shapes[1], self.shapes[0])
		return self

def between(s1, s2, pThresh=0):
	"""Finds intersections between two shapes of any type
	If two segments overlap, returns the center of the overlapping section
	Arguments:
		s1, s2: [Shape] Shapes to intersect
		pThresh: [float] The threshold of error for considering 2 lines parallel
	Returns: [list [Vector]] A list of intersection points
	"""
	sp = ShapePair(s1, s2, pThresh=pThresh)
	
	if sp.matches("polygon", "polygon"):
		return _polygonPolygon(sp)
		
	elif sp.matches("polygon", "circle"):
		return _polygonCircle(sp)
		
	elif sp.matches("circle", "circle"):
		return _circleCircle(sp)
	
def _polygonPolygon(sp):
	p1 = sp.shapes[0]
	p2 = sp.shapes[1]
	pThresh = sp.pThresh
	
	intersectList = []
	for s1 in p1.segments():
		for s2 in p2.segments():
			intersect = s1.intersect(s2, pThresh)
			if len(intersect) == 1:
				intersectList.append(intersect[0])
			elif len(intersect) == 2:
				intersectList.append(Segment(intersect[0], intersect[1]).center())
	return intersectList
	
def _polygonCircle(sp):
	sp.order("polygon")
	p = sp.shapes[0]
	c0 = sp.shapes[1]
	
	intersectList = []
	for segment in p.segments():
		c = c0.copy()
		s = segment.copy()
		
		# Maps circle's center to origin, line to horizontal
		toMove = c.center.mul(-1)
		toRotate = -s.angle()
		c.move(toMove)
		s.move(toMove)
		s.rotate(toRotate)
		
		# Calculates intersects
		segmentHeight = s.p1.y
		segmentSpan = Region(s.p1.x, s.p2.x)
		segmentPoints = []
		if abs(segmentHeight) >= abs(c.radius):
			continue
		else:
			xMaxPt = math.sqrt(c.radius ** 2 - segmentHeight ** 2)
			xMinPt = -xMaxPt
			if segmentSpan.contains(xMinPt):
				segmentPoints.append(Vector(xMinPt, segmentHeight))
			if segmentSpan.contains(xMaxPt):
				segmentPoints.append(Vector(xMaxPt, segmentHeight))
		
		# Translates solutions back to original coordinates
		for spt in segmentPoints:
			spt = spt.rotate(-toRotate)
			spt = spt.sub(toMove)
			intersectList.append(spt)
		
	return intersectList

def _circleCircle(sp):
	c1 = sp.shapes[0]
	c2 = sp.shapes[1]
	
	# Displacement between the circles
	dVector = c2.center.sub(c1.center)
	d = dVector.len()
	dAngle = dVector.angle()
	
	if d >= c2.radius + c1.radius:
		# Circles are too far apart; no intersects
		return []
	elif d <= abs(c2.radius - c1.radius):
		# One circle contains the other; no intersects
		return []
	else:
		# Aliases
		r1 = c1.radius
		r2 = c2.radius
		# Distance of intersect along displacement axis
		d1 = (d*d + r1*r1 - r2*r2) / (2*d)
		# Displacement of intersect perpendicularly from displacement axis
		y1 = math.sqrt(r1*r1 - d1*d1)
		
		# Intersections
		i1 = Vector(d1, -y1)
		i2 = Vector(d1, y1)
		i1 = i1.rotate(dAngle)
		i2 = i2.rotate(dAngle)
		i1 = i1.add(c1.center)
		i2 = i2.add(c1.center)
	
	return [i1, i2]
