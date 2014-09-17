import types

# Useful type lists
RealTypes = [types.IntType, types.LongType, types.FloatType]
ComplexTypes = RealTypes + [types.ComplexType]

# Type checkers for debugging

def reqType(a, t):
	"""Requires a to have type t
	
	Args:
		a: Any object
		t: A type
	
	Exception:
		TypeError if t is not a type
		TypeError if a is not an instance of t
	"""
	
	# Bootstrap type check
	if not isinstance(t, type):
		raise TypeError("reqType: Second argument should be type, was "+str(t))
	
	if not isinstance(a, t):
		raise TypeError("reqType: "+str(a)+" should be an instance of "+str(t))

def reqTypes(a, typeList):
	"""Requires a to have a type in list typeList
	
	Args:
		a: Any object
		typeList: The string name of a type
	
	Exception:
		TypeError if typeList is not a list of types
		TypeError if a is not an instance of anything in typeList
	"""
	
	reqType(typeList, types.ListType)
	for t in typeList:
		if not isinstance(t, type):
			raise TypeError("reqTypes: "+str(t)+" in type list is not a type")
		if isinstance(a, t): return
	raise TypeError("reqTypes: "+str(a)+" was not one of the types specified")
