# File: router.py
#
# Description: a router, with associated links and flow
# route packets to destination host
# 
# Initialization: 
#  Takes a string that is the unique router ID
#  Takes an array containing arbitrary number of strings,
#		its connected links' id's
#
# Last Revised: 9 November 2015 by Ahmed Alshaia

from node import Node
import constants

# The class Node extends the class Reporter
class Router(Node):

	link = []
	sim = ""
	dest = ""		# destination host

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
		self.routing_table = {}	
		self.default_port = None

	# dict routing_table: routing table
	# key: destination host id
	# cost tuple (distance between current router and destination host,
	# next hop)
	def initalize_routing_table(self,hosts_ids):
		self.default_port = self.links[0].dest
		# set the distance to be inf, the next hop to be the default_port
		for host_id in hosts_ids:
			cost = float('inf'),self.default_port
			self.routing_table[host_id] = cost
			# If the host destination is a neighbor, set the distance to be 1, the next hop to be host destination
		for link2 in self.links:
			if #??
			cost = 1, #??
			self.routing_table[] = cost

	def update_routing_table(self)


	def set_event_simulator (self, sim):
		self.sim = sim

	def get_link(self):
		return self.link

	def get_dest (self):
		return self.dest 
