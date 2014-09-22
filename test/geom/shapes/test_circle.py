import pytest

from sphericalcow.geom.shapes.circle import Circle
from sphericalcow.geom.region import Region
from sphericalcow.geom.shape import Shape
from sphericalcow.geom.vector import Vector
import math

c0 = Circle(Vector(0,0), 0)
c1 = Circle(Vector(5,0), 3)

def test_copy():
	assert c0.copy() == c0
	assert not c0.copy() is c0
	assert c1.copy() == c1
	assert not c1.copy() is c1

def test_equalsInRange():
	assert c0.equalsInRange(c0, .001)
	assert c0.equalsInRange(Circle(Vector(1,1),1), 1.5)

def test_rotate():
	assert c0.copy().rotate(0) == c0
	assert c1.copy().rotate(0) == c1
	assert c1.copy().rotate(math.pi * 1/2.) == c1
	
	# About
	assert c0.copy().rotate(0, about=Vector(0,0)) == c0
	assert c0.copy().rotate(math.pi * 1/2., about=Vector(1,0)).equalsInRange( \
		Circle(Vector(1,-1), 0), .01)

def test_area():
	assert c0.area() == 0
	assert abs(c1.area() - 9*math.pi) < .01

def test_area2():
	assert c0.area2() == 0
	assert abs(c1.area2() - math.pow(3,4)/2.*math.pi) < .01
	
	# About
	assert c0.area2(about=Vector(1,0)) == 0
	assert abs(c1.area2(about=Vector(5,0)) - c1.area2()) < .01
	assert abs(c1.area2(about=Vector(1,0)) - \
		(c1.area2() + 4*4*c1.area())) < .01
	
def test_shadow():
	assert c0.shadow(Vector(0,0)) == Region(0,0)
	assert c0.shadow(Vector(1,1)) == Region(0,0)
	assert c1.shadow(Vector(0,0)) == Region(0,0)
	assert c1.shadow(Vector(1,0)) == Region(2,8)
	assert c1.shadow(Vector(0,1)) == Region(-3,3)
	assert c1.shadow(Vector(0,-1)) == Region(-3,3)
	
def test_getCollisionAxes():
	s0 = Shape(Vector(0,0))
	s1 = Shape([Vector(0,-2), Vector(4,-2), Vector(4,2), Vector(0,2)])
	axes0 = c0.getCollisionAxes(s1)
	assert len(axes0) == 1
	assert axes0[0].equalsInRange(Vector(-2,0), .01)
	
	axes1 = c1.getCollisionAxes(s1)
	assert len(axes1) == 1
	assert axes1[0].equalsInRange(Vector(3,0), .01)

def test_contains():
	assert not c0.contains(Vector(1,1))
	assert not c1.contains(Vector(1,0))
	assert not c1.contains(Vector(5,5))
	assert c1.contains(Vector(5,2))
	assert c1.contains(Vector(2.1,0))

def test_intersections():
	#TODO
	pass
	