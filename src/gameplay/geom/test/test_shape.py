import pytest
import sys, os, imp
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

shape = imp.load_source('shape', 'gameplay/geom/shape.py')
from shape import Shape
from vector import Vector
from region import Region
import math

s0 = Shape([Vector(0,0)])
s1 = Shape([Vector(0,0), Vector(10,0), Vector(10,10), Vector(0,10)])

s2 = Shape([Vector(0,0), Vector(10,0), Vector(0,10)])
s3 = Shape([Vector(-5,0), Vector(5,0), Vector(5,5), Vector(-5,2)])

# Concave
s4 = Shape([Vector(0,0), \
			Vector(0,10), \
			Vector(10,10), \
			Vector(5,5), \
			Vector(10,0)])

def test_legal():
	# TODO
	pass

def test_copy():
	s0cp = s0.copy()
	s1cp = s1.copy()
	assert s0cp is not s0
	assert s1cp is not s1
	assert s0 == s0cp
	assert s1 == s1cp

def test_equalsInRange():
	s0cp = s0.copy()
	s1cp = s1.copy()
	assert not s0.equalsInRange(s1, .01)
	assert s0.equalsInRange(s0cp, .01)
	assert s1.equalsInRange(s1cp, .01)
	assert s1.equalsInRange( \
		Shape([Vector(0.1, 0.1), Vector(10.1, -0.1), Vector(10.1, 9.9), Vector(0.1, 10.2)]), \
		0.5)
	assert not s0.equalsInRange(Shape([Vector(0.5, 0)]), 0.4)

def test_com():
	assert s0.com().equalsInRange(Vector(0,0), .01)
	assert s1.com().equalsInRange(Vector(5,5), .01)

def test_move():
	assert s0.copy().move(Vector(0,0)).points == [Vector(0,0)]
	assert s0.copy().move(Vector(10,10)).points == [Vector(10,10)]
	assert s1.copy().move(Vector(0,0)).points == s1.points
	assert s1.copy().move(Vector(10,10)).points == \
		[Vector(10,10), Vector(20,10), Vector(20,20), Vector(10,20)]

def test_rotate():
	assert s0.copy().rotate(0).equalsInRange(s0, .01)
	assert s0.copy().rotate(math.pi).equalsInRange(s0, .01)
	assert s1.copy().rotate(0).equalsInRange(s1, .01)
	assert s1.copy().rotate(math.pi / 2).equalsInRange( \
		Shape([Vector(10,0), Vector(10,10), Vector(0,10), Vector(0,0)]), .01)
	assert s1.copy().rotate(- math.pi / 2).equalsInRange( \
		Shape([Vector(0,10), Vector(0,0), Vector(10,0), Vector(10,10)]), .01)
	
	# About
	assert s1.copy().rotate(0, Vector(0,0)).equalsInRange(s1, .01)
	assert s1.copy().rotate(math.pi, Vector(0,0)).equalsInRange( \
		Shape([Vector(0,0), Vector(-10,0), Vector(-10,-10), Vector(0,-10)]), .01)

def test_area():
	assert s0.area() == 0
	assert s1.area() == 100
	assert s2.area() == 50
	assert s3.area() == 35

def test_area2():
	assert s0.area2() == 0
	assert abs(s1.area2() - 100) < .01
	assert abs(s2.area2() - 66.67) < .01
	assert abs(s3.area2() - 58.38) < .01

def test_shadow():
	assert s0.shadow(Vector(1,0)) == Region(0,0)
	assert s1.shadow(Vector(0,0)) == Region(0,0)
	assert s1.shadow(Vector(1,0)) == Region(0,10)
	assert s1.shadow(Vector(-1,0)) == Region(0,10)
	assert s1.shadow(Vector(100,0)) == Region(0,10)
	assert s1.shadow(Vector(0,9.9)) == Region(0,10)
	assert abs(s1.shadow(Vector(1,1)).right - 10*math.sqrt(2)) < .01

def test_getCollisionAxes():
	# Argument does not matter -- default shape's axes are not collision dependent
	
	l0 = s0.getCollisionAxes(s0)
	assert len(l0) == 1
	assert l0[0] == Vector(0,0)
	
	l1 = s1.getCollisionAxes(s0)
	assert len(l1) == 4
	assert l1[0].equalsInRange(Vector(0, 1), .01)
	assert l1[1].equalsInRange(Vector(-1, 0), .01)
	assert l1[2].equalsInRange(Vector(0, -1), .01)
	assert l1[3].equalsInRange(Vector(1, 0), .01)

def test_mtv():
	assert s0.mtv(s1) == Vector(0,0)
	assert s1.mtv(s0) == Vector(0,0)
	assert s1.mtv(s1).len() == 10
	assert s1.mtv(s2).equalsInRange(Vector(5,5), .01)
	assert s2.mtv(s1).equalsInRange(Vector(-5,-5), .01)
	assert s1.mtv(s1.copy().move(Vector(10.1,0))) == Vector(0,0)
	assert s1.mtv(s1.copy().move(Vector(9.9,0))).equalsInRange(Vector(.1,0), .01)
	
def test_contains():
	assert not s0.contains(Vector(1,1))
	assert not s1.contains(Vector(-1,1))
	assert not s1.contains(Vector(1,-1))
	assert not s1.contains(Vector(-1,-1))
	assert s1.contains(Vector(1,1))
	assert s1.contains(Vector(9,9))
	assert not s1.contains(Vector(19,9))
	assert not s2.contains(Vector(5,6))
	assert s2.contains(Vector(4.5,4.5))
	assert s2.contains(Vector(4.5,4.5))
	
	# Concave
	assert not s4.contains(Vector(6,5))
	assert s4.contains(Vector(4,5))
	assert s4.contains(Vector(7,8))
	assert s4.contains(Vector(7,2))
	assert not s4.contains(Vector(7,20))
	assert not s4.contains(Vector(7,-2))

def test_intersections():
	assert len(s0.intersections(s0)) == 0
	assert len(s1.intersections(s0)) == 0
	s1s1 = s1.intersections(s1, pThresh=.001)
	assert len(s1s1) == 4
	assert s1s1[0].equalsInRange(Vector(5,0), .001)
	assert s1s1[1].equalsInRange(Vector(10,5), .001)
	assert s1s1[2].equalsInRange(Vector(5,10), .001)
	assert s1s1[3].equalsInRange(Vector(0,5), .001)
	assert len(s1.copy().move(Vector(1,1)).intersections(s1)) == 2
	
