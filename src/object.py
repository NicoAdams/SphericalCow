from geom.shape import shape

class ObjectDef:
	"""Stores the information defining an object
	Fields:
		dynamic: True if object can respond to forces, else False
		solid: True if object can interact with others, else False
		shape: The Shape defining the object
		friction: The friction coefficient (0-1)
		restitution: The "bounciness" coefficient (0-1)
	"""
	def __init__():
		self.dynamic = False
		self.solid = True
		self.shape = Shape()
		self.friction = 0
		self.restitution = 0
		
class Object:
	"""Represents a physics object
	"""
	
	def __init__(self, def):
		"""
		Arguments:
			def: [ObjectDef] An object definition
		"""
		self.shape = def.shape
		self.solid = def.solid
		self.shape = def.shape
		self.friction = def.friction
		self.restitution = def.restitution
	
