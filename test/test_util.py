import pytest

from sphericalcow import util
import types

# Sets up an equalsInRange testing class
class testClass:
	def __init__(self, value):
		self.value = value
	
	def equalsInRange(self, other, error):
		return abs(self.value - other.value) < error

def test_reqType():
	# Successful type checks
	assert util.reqType(1, type(1)) == None
	assert util.reqType('a', types.StringType) == None
	
	# Unsuccessful type check
	pytest.raises(TypeError, util.reqType, *('a', types.IntType))
	
	# Invalid input
	pytest.raises(TypeError, util.reqType, *(1, 2))
	
def test_reqTypes():
	# Successful type checks
	assert util.reqTypes(1, util.RealTypes) == None
	assert util.reqTypes(complex("j"), util.ComplexTypes) == None
	assert util.reqTypes('asdf', list(types.StringTypes)) == None
	assert util.reqTypes('asdf', [types.StringType]) == None
	
	# Failed type checks
	pytest.raises(TypeError, util.reqTypes, *('a', util.RealTypes))
	pytest.raises(TypeError, util.reqTypes, *(complex('j'), util.RealTypes))
	pytest.raises(TypeError, util.reqTypes, *(1, []))
	
	# Invalid input
	pytest.raises(TypeError, util.reqTypes, *(1, types.StringType))
	pytest.raises(TypeError, util.reqTypes, *(1, 2))
	pytest.raises(TypeError, util.reqTypes, *(1, [2,3]))

def test_listEqualsInRange():
	l0 = []
	# Standard
	l1 = [testClass(1), testClass(2), testClass(3)]
	# Equal
	l2 = [testClass(2 + .01), testClass(3 - .01), testClass(1)]
	# Unequal -- different elements
	l3 = [testClass(2 + .01), testClass(2 - .01), testClass(1 + .01)]
	# Unequal -- different length
	l4 = [testClass(1 + .01), testClass(2 + .01), testClass(3 - .01), testClass(4 + .01)] 
	
	assert util.listEqualsInRange(l0, l0, .05)
	assert util.listEqualsInRange(l1, l1, .05)
	assert util.listEqualsInRange(l1, l2, .05)
	assert util.listEqualsInRange(l2, l1, .05)
	assert not util.listEqualsInRange(l1, l0, .05)
	assert not util.listEqualsInRange(l1, l3, .05)
	assert not util.listEqualsInRange(l1, l4, .05)
	assert not util.listEqualsInRange(l4, l1, .05)
	