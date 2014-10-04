from geom.shape import shape

# Do I want to make this a dict?
class ObjectDef:
	"""Stores the information defining an object
	Fields:
		pos: [Vector] The object's position
		vel: [Vector] The object's velocity
		rot: [Vector] The object's rotation
		rvel: [Vector] The object's angular velocity
		dynamic: [bool] True if object can respond to forces, else False
		solid: [bool] True if object can interact with others, else False
		shape: [Shape] The Shape defining the object
		friction: [float] The friction coefficient (0-1)
		restitution: [float] The "bounciness" coefficient (0-1)
	"""
	def __init__():
		self.pos = Vector(0,0)
		self.vel = Vector(0,0)
		self.rot = 0
		self.rvel = 0
		self.dynamic = False
		self.solid = True
		self.shape = Shape()
		self.density = 1
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
		self.pos = def.pos
		self.vel = def.vel
		self.rot = def.rot
		self.rvel = def.rvel
		self.shape = def.shape
		self.solid = def.solid
		self.shape = def.shape
		self.density = def.density
		self.friction = def.friction
		self.restitution = def.restitution
	
	def com(self):
		return self.shape.com()
	
	# Define getters for all your properties
	
	def move(self, toMove):
		"""
		Arguments:
			toMove: [Vector] Amount to move
		"""
		self.shape.move(toMove)
		return self
	
	def rotate(self, toRotate):
		"""
		Arguments:
			toRotate: [float] Angle to rotate
		"""
		self.shape.rotate(toRotate)
		return self
	
	def mass(self):
		"""
		Arguments:
			toMove: [Vector] Amount to move
		"""
		return self.shape.area() * self.density
	
	def angMass(self, about=None):
		"""
		Arguments:
			toMove: [Vector] Amount to move
		"""
		if about is None: about = self.com()
		return self.shape.area2(about)
	
	def localVel(self, about, direction):
		"""Returns calculated local mass value
		Arguments:
			about: [Vector] The point about which to calculate
			direction: [Vector] The direction about which to calculate
		"""
		disp = about.sub(self.com())
		localVel = self.vel.add(disp.rotate(-math.pi/2).mul(self.rot))
		return localVel.
	
	def localMass(self, about):
		"""Returns calculated local mass value
		Arguments:
			about: [Vector] The point about which to calculate
		"""
	
	def applyImpulse(self, impulse, point):
		"""
		Arguments:
			impulse: [Vector] The impulse amount and direction
			point: [Vector] The point of impulse exertion
		"""
		
