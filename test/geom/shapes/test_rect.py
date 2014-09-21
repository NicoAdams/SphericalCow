import pytest

from sphericalcow.geom.shapes.rect import Rect
from sphericalcow.geom.shape import Shape
from sphericalcow.geom.vector import Vector

def test_init():
	assert Rect(0,0,1,1,0).equalsInRange( \
		Shape([Vector(0,0), Vector(1,0), Vector(1,1), Vector(0,1)]), \
		.01)