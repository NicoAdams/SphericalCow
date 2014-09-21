import pytest

from sphericalcow.geom.vector import Vector, fromPolar
import math

v0 = Vector(0,0)
v1 = Vector(3,4)
v2 = Vector(5,-12)
v3 = Vector(0,5.1)
v4 = Vector(-1000.5,0)
v5 = Vector(0,-.011)

def test_equalsInRange():
	assert v0.equalsInRange(v0, 0.01)
	assert v1.equalsInRange(v1, 0.01)
	assert v1.equalsInRange(Vector(v1.x+0.1, v1.y), 0.2)
	assert v1.equalsInRange(Vector(v1.x-0.1, v1.y), 0.2)
	assert not v1.equalsInRange(Vector(v1.x+0.5, v1.y), 0.2)
	assert v1.equalsInRange(Vector(v1.x, v1.y+0.1), 0.2)
	assert v1.equalsInRange(Vector(v1.x, v1.y-0.1), 0.2)
	assert not v1.equalsInRange(Vector(v1.x, v1.y+0.5), 0.2)

def test_len():
	assert v0.len() == 0
	assert v1.len() == 5
	assert v2.len() == 13

def test_angle():
	assert v0.angle() == 0
	assert v3.angle() == math.pi * 1/2
	assert v4.angle() == math.pi
	assert v5.angle() == - math.pi * 1/2

def test_mul():
	assert v0.mul(1) == Vector(0,0)
	assert v1.mul(0) == Vector(0,0)
	assert v1.mul(1) == Vector(3,4)
	assert v1.mul(10) == Vector(30,40)

def test_norm():
	assert v0.norm() == Vector(0, 0)
	assert v1.norm().len() == 1 and \
			v1.norm().angle() == v1.angle()
	assert v2.norm().len() == 1 and \
			v2.norm().angle() == v2.angle()
	assert v3.norm().len() == 1 and \
			v3.norm().angle() == v3.angle()

def test_add():
	assert v0.add(v1) == v1
	assert v1.add(v0) == v1
	assert v1.add(v1) == Vector(6,8)

def test_sub():
	assert v0.sub(v1) == Vector(-3,-4)
	assert v1.sub(v0) == v1
	assert v1.sub(v1) == v0
	
def test_dot():
	assert v0.dot(v1) == 0
	assert v1.dot(v0) == 0
	assert v1.dot(v1) == 25
	assert v2.dot(v1) == -33

def test_scalarCross():
	assert v0.scalarCross(v0) == 0
	assert v0.scalarCross(v1) == 0
	assert v1.scalarCross(v0) == 0
	assert v1.scalarCross(v1) == 0
	assert v3.scalarCross(v4) == 5.1 * 1000.5

def test_rotate():
	assert v0.rotate(math.pi) == v0
	assert v1.rotate(0).equalsInRange(v1, .01)
	assert v1.rotate(math.pi * 1/2).equalsInRange(Vector(-4,3), .01)
	assert v1.rotate(math.pi * 2/2).equalsInRange(Vector(-3,-4), .01)
	assert v1.rotate(math.pi * 3/2).equalsInRange(Vector(4,-3), .01)

def test_rotateAbout():
	assert v0.rotateAbout(math.pi, v0) == v0
	assert v1.rotateAbout(0, v0).equalsInRange(v1, .01)
	assert v1.rotateAbout(math.pi * 1/2, v0).equalsInRange(Vector(-4,3), .01)
	assert v1.rotateAbout(math.pi * 1/2, v1).equalsInRange(Vector(3,4), .01)
	assert v0.rotateAbout(math.pi * 1/2, v1).equalsInRange(Vector(7,1), .01)

def test_project():
	assert v0.project(v0) == v0
	assert v1.project(v0) == v0
	assert v0.project(v1) == v0
	assert v1.project(v1).equalsInRange(v1, .01)
	assert v1.project(Vector(10.5,0)).equalsInRange(Vector(3, 0), .01)
	assert v1.project(Vector(-10.5,0)).equalsInRange(Vector(3, 0), .01)
	assert v1.project(Vector(0,100)).equalsInRange(Vector(0, 4), .01)
	assert v1.project(v1.rotate(math.pi/2)).equalsInRange(v0, .01)

def test_limit():
	assert v0.limit(v0, 1) == v0
	assert v0.limit(v1, 1) == v0
	assert v1.limit(v1, 0).equalsInRange(v0, .01)
	assert v1.limit(v0, 1) == v1
	assert v1.limit(v1, -1) == v1
	assert v1.limit(Vector(234, 0), 1).equalsInRange(Vector(1, 4), .01)

def test_from_polar():
	assert fromPolar(0, 0) == Vector(0,0)
	assert fromPolar(1, 0).equalsInRange(Vector(1,0), .01)
	assert fromPolar(1, math.pi/4).equalsInRange(Vector(math.sqrt(2)/2, math.sqrt(2)/2), .01)
	assert fromPolar(10, 3*math.pi/2).equalsInRange(Vector(0, -10), .01)
