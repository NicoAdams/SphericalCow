import objects.object_group.ObjectGroup
import objects.object.Object

class WorldObjects:
	"""Has an active layer and a dict of background layers
	"""
	
	def __init__(self):
		self.active = ObjectGroup()
		self.background = {} # depth (positive float) -> ObjectGroup
	
