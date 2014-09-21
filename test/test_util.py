import pytest

from sphericalcow import util
import types

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
