import pytest

from sphericalcow import util
import types

# Sets up an equalsInRange testing class
class testClass:
	def __init__(self, value):
		self.value = value
	
	def __eq__(self, other):
		return self.value == other.value
	
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

def test_listEquals():
	assert util.listEquals([], [])
	# Identity
	assert util.listEquals([1,2,3], [1,2,3])
	# Equal
	assert util.listEquals([1,2,3], [2,3,1])
	# Input should be symmetric
	assert util.listEquals([2,3,1], [1,2,3])
	# Different lengths
	assert not util.listEquals([1,2,3], [1,2,3,4])
	# Different elements
	assert not util.listEquals([1,2,3], [2,3,4])
	# Input should be symmetric
	assert not util.listEquals([2,3,4], [1,2,3])
	
	# Arbitrary equality function
	def eqPlus1(e1,e2):
		return e1+1 == e2
	assert util.listEquals([1,2,3], [3,4,2], eqFunction=eqPlus1)

def test_listEqualsInRange():
	l0 = []
	# Standard
	l1 = [testClass(1), testClass(2), testClass(3)]
	l2 = [testClass(2 + .01), testClass(3 - .01), testClass(1)]
	l3 = [testClass(2 + .01), testClass(2 - .01), testClass(1 + .01)]
	l4 = [testClass(1 + .01), testClass(2 + .01), testClass(3 - .01), testClass(4 + .01)] 
	
	assert util.listEqualsInRange(l0, l0, .05)
	# Identical lists
	assert util.listEqualsInRange(l1, l1, .05)
	# Equal lists
	assert util.listEqualsInRange(l1, l2, .05)
	# Input should be symmetric
	assert util.listEqualsInRange(l2, l1, .05)
	# Different elements
	assert not util.listEqualsInRange(l1, l3, .05)
	# Different lengths
	assert not util.listEqualsInRange(l1, l4, .05)
	# Input should be symmetric
	assert not util.listEqualsInRange(l4, l1, .05)
	