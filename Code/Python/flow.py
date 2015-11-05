# flow Code
# Sith Domrongkitchaiporn

from reporter import Reporter

# This class only extends Reporter Class
class Flow(Reporter):
	source = ""
	dest = ""
	size = -1
	start =  -1
	sim = ""

	# Call Node initialization code, with the Node ID (required unique)
	# Initializes itself
	def __init__(self, identity, src, sink, size, start):
		Reporter.__init__(self, identity)
		self.source = src
		self.dest = sink
		self.size = int(size)
		self.start = int(start)

	def set_event_simulator (self, sim):
		self.sim = sim

	def get_source (self):
		return self.source

	def get_dest (self):
		return self.dest  

	def get_size (self):
		return self.size  

	def get_start (self):
		return self.start  