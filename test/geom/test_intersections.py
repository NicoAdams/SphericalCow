import pytest

from sphericalcow.geom.shape import Shape
from sphericalcow.geom.vector import Vector
from sphericalcow.geom.shapes.circle import Circle
import sphericalcow.geom.intersections as intersections
from sphericalcow.util import listEqualsInRange

s0 = Shape([Vector(0,0)])
s1 = Shape([Vector(0,0), Vector(10,0), Vector(10,10), Vector(0,10)])
s2 = Shape([Vector(0,0), Vector(10,0), Vector(0,10)])

c0 = Circle(Vector(0,0), 0)
c1 = Circle(Vector(5,0), 5)
c2 = Circle(Vector(-1,0), 5)
c3 = Circle(Vector(-3,0), 2)
c4 = Circle(Vector(4,0), 3)

def test_polygonPolygon():
	assert len(intersections.between(s0,s0)) == 0
	assert len(intersections.between(s0,s1)) == 0
	s1s1 = intersections.between(s1, s1, pThresh=.001)
	assert len(s1s1) == 4
	assert listEqualsInRange(s1s1, \
		[Vector(5,0), Vector(10,5), Vector(5,10), Vector(0,5)], .001)
	s1s1c = intersections.between(s1.copy().move(Vector(1,1)), s1)
	assert len(s1s1c) == 2
	assert listEqualsInRange(s1s1c, \
		[Vector(10,1), Vector(1,10)], .001)
	
	# Literally a corner case
	s1s2 = intersections.between(s1, s2)
	assert len(s1s2) == 2
	assert listEqualsInRange(s1s2, \
		[Vector(0,5), Vector(5,0)], .001)

def test_polygonCircle():
	# Corner
	s1c1 = intersections.between(s1, Circle(Vector(0,0), 2))
	assert len(s1c1) == 2
	assert listEqualsInRange(s1c1, \
		[Vector(2,0), Vector(0,2)], .01)
	# Edge
	s1c2 = intersections.between(s1, Circle(Vector(-4,5), 5))
	assert len(s1c2) == 2
	assert listEqualsInRange(s1c2,
		[Vector(0,2), Vector(0,8)], .01)
	# No intersect
	s1c3 = intersections.between(s1, Circle(Vector(-4, 5), 3))
	assert len(s1c3) == 0
	
def test_circleCircle():
	assert len(intersections.between(c0,c0)) == 0
	assert len(intersections.between(c1,c0)) == 0
	assert len(intersections.between(c1,c1)) == 0
	# Intersections
	c1c2 = intersections.between(c1, c2)
	assert len(c1c2) == 2
	assert listEqualsInRange(c1c2, \
		[Vector(2,4), Vector(2,-4)], .01)
	# Outside
	c1c3 = intersections.between(c1,c3)
	assert len(c1c3) == 0
	# Inside
	c1c4 = intersections.between(c1,c4)
	assert len(c1c4) == 0
	# Angled
	c1c1c = intersections.between( \
		c1, c1.copy().move(Vector(-5, 5)))
	assert len(c1c1c) == 2
	assert listEqualsInRange(c1c1c, \
		[Vector(5,5), Vector(0,0)], .01)
