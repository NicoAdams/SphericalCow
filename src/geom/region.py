class Region(object):
	"""Represents a 2D region with a left and right
	Inclusive on the left, exclusive on the right
	"""
	
	def __init__(self, val1, val2):
		"""
		Arguments:
			val1: [float] A value
			val2: [float] A value
		Returns: Region with [left, right] chosen from [val1, val2]
		"""
		self.right = max(val1, val2)
		self.left = min(val1, val2)
	
	def __eq__(self, other):
		return self.left == other.left and self.right == other.right
	
	def len(self):
		return self.right - self.left
	
	def center(self):
		return (self.right + self.left)/2
	
	def contains(self, num):
		return num < self.right and num > self.left
	
	def overlaps(self, other):
		return not (other.left >= self.right) and not (other.right <= self.left)
	
	def overlapRegion(self, other):
		# Returns False if self and other do not overlap
		if not self.overlaps(other): return False
		return Region(max(self.left, other.left), min(self.right, other.right))
	
	def minTranslation(self, other):
		# Returns the minimum translation distance needed to offset other from self
		if not self.overlaps(other):
			return 0
		if self.center() <= other.center():
			return self.right - other.left
		return self.left - other.right
	
		