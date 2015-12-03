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
# Last Revised: 23 November 2015 by Ahmed Alshaia

from node import Node
import constants
from packet import *
from jsonparser import *

# The class Node extends the class Reporter
class Router(Node):

	link = []
	sim = ""
	# dest = ""		# destination host

	# Routing Tables
	# - Current one
	# - a new one currently under construction  
	current = {}
	new = {}

	itr = 0 # number of iterations of b-f

	# Call Node initialization code, with the Node ID (required unique)
	# Initializes itself
	def __init__(self, identity, links):
		Node.__init__(self, identity)				
		self.link = links
		self.current = {}	# Current Routing table
		self.new = {}		# Routing table under construction	
		self.itr = 0


	''' table
		key: destination (string ID)
		value: link (string ID)
	'''
	def static_routing(self, table):
		self.current = table

	'''
	Receive takes care of Packet Types
	- Data/Ack: Forward packets along
	- Router: Create Router_Ack + new_table
	- Ack: Update table using the newly received table
	'''
	def receive(self, packet):
		p = packet.get_type()
		if (p == DATA_PACKET_TYPE) or (p == DATA_PACKET_ACKNOWLEDGEMENT_TYPE):
			self.send(packet)
		elif (p == ROUTER_PACKET_TYPE):		# Create an ACK packet and send back routing info
			link = packet.get_link()
			q = Router_Packet(ROUTER_FLOW, self.get_id(), packet.get_source(), ROUTER_PACKET_ACKNOWLEDGEMENT_TYPE, ROUTER_FLOW, DATA_ROUTER_ACK_BITWIDTH, link)
			q.set_routing_map(self.new)
			self.send(q)
		elif (p == ROUTER_PACKET_ACKNOWLEDGEMENT_TYPE):
			self.update_routing_table(packet,jsonparser.get_total_links())	# check argument q

	# Routing table is a String table with a String key
	# The key is the final destination
	# The value is the link
	def send(self, packet):
		p = packet.get_type()
		if (p == DATA_PACKET_TYPE) or (p == DATA_PACKET_ACKNOWLEDGEMENT_TYPE): 
			# Current is a dict.  We are trying to get the packet destination which is the dict key
			# next_dest is a String of the link that should be sent to		
			next_dest = self.current[packet.get_dest()][1] # a link
			self.sim.get_element(next_dest).send(packet, self.get_id())	
			# self.log("Sent packet id %d of type %s to %s" % (packet.get_ID(), packet.get_type(), next_dest))
		elif (p == ROUTER_PACKET_TYPE):
			link = self.sim.get_element(packet.get_link())
			link.send(packet, self.get_id())
		elif (p == ROUTER_PACKET_ACKNOWLEDGEMENT_TYPE):
			# Create a cost for traveling through the link
			link = self.sim.get_element(packet.get_link())
			packet.set_cost(link.get_delay() + (link.get_rate()*link.get_occupancy()))
			link.send(packet, self.get_id())

	# Initialize routing table by creating keys for all hosts in the test case
	# The value of the table is a tuple (distance between current router and destination host, next hop(link))
	# Initially, set the distance to be inf, the next hop to link[0]
	# host_ids is an array contains all host ids
	def initalize_routing_table(self):
		
		for host_id in jsonparser.get_host_array()
			value = float('inf'),self.links[0] # a default link
			self.new[host_id] = value
		# If the host destination is directly connected to the router (neighbor), set the distance to 0 and next hop to corresponiding link
		for link2 in self.link:
			for key in self.new:
				if (key == self.sim.get_element(link2).get_left()) or (key == self.sim.get_element(link2).get_right()):
					value = 0, link2 # this link
					self.new[key] = value
		# Send first iteration of router packet
		for link2 in self.link:
			if self.sim.get_element(link2).get_left() == self.get_id():  # If the router is on the left, sink is on the right
				sink = self.sim.get_element(link2).get_right()
			else:
				sink = self.sim.get_element(link2).get_left()			 # If the router is on the right, sink is on the left
			packet = Router_Packet(ROUTER_FLOW,self.get_id(),sink,ROUTER_PACKET_TYPE,ROUTER_FLOW,DATA_ROUTER_BITWIDTH,link2)
			self.send(packet)

	# Implement Bellman-Ford algorithm
	# Compare router table from acknowledgement of router packet received from neighbor routers and the current router. 
	# Update router table if there is a shorter path.
	# Static routing: metric based on hops (1 hop for each link)
	# Dynamic routing: metric based on link cost
	def update_routing_table(self, router_packet,total_links):
		for (d,v) in router_packet.get_routing_map().items(): # every item in routing table
			if STATIC_ROUTING:

			else: #dynamic routing
				metric = router_packet.get_cost() #link cost
				if v[0] + metric < self.new [d][0]:
						new_v = v[0] + metric , self.new[d][1] 
						self.new[d] = new_v
		self.itr = self.itr + 1

		# Send next iteration of router packet
		if (self.itr <= total_links):			
			for link2 in self.link:
				if self.sim.get_element(link2).get_left() == self.get_id():
					sink = self.sim.get_element(link2).get_right()
				else:
					sink = self.sim.get_element(link2).get_left()
				packet = Router_Packet(ROUTER_FLOW,self.get_id(),sink,ROUTER_PACKET_TYPE,ROUTER_FLOW,DATA_ROUTER_BITWIDTH,link2)
				self.send(packet)
		else:
			self.current = self.new
			self.itr = 0
	
	'''
	def routing_table_periodic_update():
		# Updates outdated routing table periodically.
		# ROUTING_TABLE_UPDATE_PERIOD
	'''

	def set_event_simulator (self, sim):
		self.sim = sim

	def get_link(self):
		return self.link

	def get_dest (self):
		return self.dest 
