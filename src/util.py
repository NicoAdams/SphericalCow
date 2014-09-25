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

def listEquals(list1, list2, eqFunction=None):
	"""Tests to see if list1 and list2 contain the same elements (in any order)
	by testing for equality
	
	Arguments:
		list1, list2: [list [E]] Lists of objects
		eqFunction: [[E],[E] -> [bool]] A function that returns true if its
			inputs are equal and false if not (default: e1, e2 -> e1==e2)
	Returns: [bool] True if list1 and list2 contain the same elements
	"""
	if len(list1) != len(list2):
		return False
	
	l1 = list(list1)
	l2 = list(list2)
	
	# Utility function to find the matching element
	def matchIndex(index):
		e1 = l1[index]
		for i2 in range(len(l2)):
			e2 = l2[i2]
			
			equal = False
			if eqFunction is None:
				equal = (e1 == e2)
			else:
				equal = eqFunction(e1, e2)
			
			if equal: return i2
		return -1
	
	while len(l1) > 0:
		i2 = matchIndex(0)
		if i2 == -1:
			return False
		l1.pop(0)
		l2.pop(i2)
	return True


def listEqualsInRange(list1, list2, error):
	"""Tests to see if list1 and list2 contain the same elements (in any order)
	with equality determined by the "equalsInRange" function
	
	Arguments:
		list1, list2: [list] Lists of objects that implement "equalsInRange()"
		error: [float] The acceptable error range
	Returns: [bool] True if list1 and list2 contain the same elements
	"""
	
	def rangeEqFunction(e1, e2):
		return e1.equalsInRange(e2, error)
	return listEquals(list1, list2, eqFunction=rangeEqFunction)

