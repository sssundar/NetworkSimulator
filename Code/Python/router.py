# Router Code
# Sith Domrongkitchaiporn

from node import Node

# The class Node extends the class Reporter
class Router(Node):

	link = []
	sim = ""

	# Routing Tables    
	# - Current one
	# - a new one currently under construction  
	current = {}
	new = {}

	# Call Node initialization code, with the Node ID (required unique)
	# Initializes itself
	def __init__(self, identity, links):
		Node.__init__(self, identity)				
		self.link = links

	def set_event_simulator (self, sim):
		self.sim = sim

	def get_link(self):
		return self.link