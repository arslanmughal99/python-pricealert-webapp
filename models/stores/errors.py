class StoreErrors(Exception):
	def __init__(self,message):
		self.message = message




class StoreNotFoundException(StoreErrors):
	pass