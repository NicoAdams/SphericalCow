import pytest
import sys, os, imp
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

segment = imp.load_source('segment', 'gameplay/geom/segment.py')
from segment import Segment
from vector import Vector
import math

s0 = Segment(Vector(0,0), Vector(0,0))
s1 = Segment(Vector(0,0), Vector(3,4))
s2 = Segment(Vector(1,0), Vector(2,5))
s3 = Segment(Vector(-3,-1), Vector(1,1))
s4 = Segment(Vector(-1,-1), Vector(-1,1))

s5 = Segment(Vector(1,3), Vector(5,3))
s6 = Segment(Vector(3,3), Vector(7,3))
s7 = Segment(Vector(0,0), Vector(10,0))

def test_equalsInRange():
	assert s0.equalsInRange(s0, .01)
	assert not s0.equalsInRange(s1, .01)
	assert s0.equalsInRange(s1, 5)
	assert s1.equalsInRange(Segment(s1.p2, s1.p1), .01)

def test_copy():
	s0cp = s0.copy()
	s1cp = s1.copy()
	assert s0cp is not s0
	assert s1cp is not s1
	assert s0 == s0cp
	assert s1 == s1cp

def test_len():
	assert s0.len() == 0
	assert abs(s1.len() - 5) < .01
	assert abs(s2.len() - math.sqrt(1 + 25)) < .01
	
def test_angle():
	assert s0.angle() == 0
	assert (s1.angle() - .59) < .01
	assert (s2.angle() - 1.57) < .01

def test_center():
	assert s0.center() == Vector(0,0)
	assert s1.center() == Vector(1.5,2)
	assert s2.center() == Vector(1.5,2.5)
	assert s3.center() == Vector(-1,0)
	assert s4.center() == Vector(-1,0)
	
def test_translate():
	print "0:", str(s1)
	assert s0.copy().translate(Vector(0,0)) == \
		Segment(Vector(0,0), Vector(0,0))
	assert s0.copy().translate(Vector(1,1)) == \
		Segment(Vector(1,1), Vector(1,1))
	assert s1.copy().translate(Vector(1,10)) == \
		Segment(Vector(1,10), Vector(4,14))

def test_rotate():
	assert s0.copy().rotate(0) == s0
	assert s0.copy().rotate(math.pi * 1./2) == s0
	assert s1.copy().rotate(0).equalsInRange(s1, .01)
	assert s1.copy().rotate(math.pi * 1./2).equalsInRange( \
		Segment(Vector(0,0), Vector(-4,3)), .01)
	
	# About
	assert s0.copy().rotate(math.pi * 1./2, Vector(1,1)).equalsInRange( \
		Segment(Vector(2,0), Vector(2,0)), .01)
	assert s1.copy().rotate(math.pi * 1./2, Vector(1,1)).equalsInRange( \
		Segment(Vector(2,0), Vector(-2,3)), .01)
	
def test_intersect():
	# Non-intersects
	assert len(s0.intersect(s1)) == 0
	assert len(s0.intersect(s0)) == 0
	assert len(s2.intersect(s3)) == 0
	
	# Point intersects
	assert len(s1.intersect(s2)) == 1
	assert s1.intersect(s2)[0].equalsInRange(Vector(15./11, 20./11), .01)
	assert len(s3.intersect(s4)) == 1
	assert s3.intersect(s4)[0].equalsInRange(Vector(-1, 0), .01)
	
	# Segment intersects
	s1s1 = s1.intersect(s1)
	assert len(s1s1) == 2
	assert Segment(s1s1[0], s1s1[1]).equalsInRange(s1, .01)
	s5s6 = s5.intersect(s6, pThresh=.001)
	assert len(s5s6) == 2
	assert Segment(s5s6[0], s5s6[1]).equalsInRange( \
		Segment(Vector(3,3), Vector(5,3)), .01)
	
def test_overUnder():
	# Over
	assert s1.overUnder(Vector(1,3)) == 1
	# Under
	assert s1.overUnder(Vector(2,1)) == -1
	# On
	assert s1.overUnder(s1.center(), onThresh=.001) == 1
	# Out of range (right)
	assert s1.overUnder(Vector(3.1, 5)) == 0
	# Out of range (left)
	assert s1.overUnder(Vector(-.1, 5)) == 0
	# On segment (perfectly vertical)
	assert s4.overUnder(Vector(-1,0), onThresh=.001) == 0
	# Over segment (perfectly horizontal)
	assert s7.overUnder(Vector(1,1)) == 1
	# Under segment (perfectly horizontal)
	assert s7.overUnder(Vector(1,-11)) == -1
