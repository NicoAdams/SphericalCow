import math
import numpy

class Vector:
	"""A 2D vector
	"""
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
	
	def __str__(self):
		printX = numpy.round(self.x, 3)
		printY = numpy.round(self.y, 3)
		return "V("+str(printX)+", "+str(printY)+")"
	
	def equalsInRange(self, other, error):
		return abs(self.x - other.x) <= error \
			and abs(self.y - other.y) <= error
	
	def len(self):
		return math.sqrt((self.x * self.x) + (self.y * self.y))
	
	def angle(self):
		return math.atan2(self.y, self.x)
	
	def mul(self, m):
		return Vector(self.x * m, self.y * m)
	
	def norm(self):
		if self.len() == 0: return Vector(0,0)
		return self.mul(1/self.len())
	
	def add(self, other):
		return Vector(self.x + other.x, self.y + other.y)
	
	def sub(self, other):
		return self.add(other.mul(-1))
	
	def dot(self, other):
		return self.x * other.x + self.y * other.y
	
	def scalarCross(self, other):
		"""
		Arguments:
			other: [Vector] The vector to cross with
		Returns: [float] The length of the cross product
		"""
		return self.x * other.y - self.y * other.x
	
	def rotate(self, theta):
		"""
		Arguments:
			theta: [float] The rotation angle
		Returns: [Vector] The vector rotated about about (0,0)
		"""
		angle = self.angle()
		length = self.len()
		return fromPolar(length, angle+theta)
	
	def rotateAbout(self, theta, about):
		"""
		Arguments:
			theta: [float] The rotation angle
			about: [Vector] The rotation point
		Returns: [Vector] The vector rotated about 'about' by angle
		"""
		dv = self.sub(about)
		return dv.rotate(theta).add(about)
		
	def project(self, other):
		"""
		Arguments:
			other: [Vector] The vector to project onto
		Returns: The projection of this vector onto other
		"""
		pv = other.norm()
		return fromPolar(self.dot(pv), pv.angle())
	
	def limit(self, axis, maxLen):
		"""
		Arguments:
			axis: [Vector] The axis of limitation
			maxLen: [float] The maximum length of the limited vector on axis
		Returns: [Vector] The vector with component parallel to axis limited to maxLen
		"""
		# Filters input
		if maxLen < 0 or axis.len() == 0: return self
		
		current = self.project(axis)
		limited = current.norm().mul(min(current.len(), maxLen))
		return self.sub(current).add(limited)
	
# Utility vector methods

def fromPolar(r, theta):
	return Vector(r*math.cos(theta),r*math.sin(theta))
	
