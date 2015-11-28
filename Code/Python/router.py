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

	# Call Node initialization code, with the Node ID (required unique)
	# Initializes itself
	def __init__(self, identity, links):
		Node.__init__(self, identity)				
		self.link = links
		self.current = {}	# Current Routing table
		self.new = {}		# Routing table under construction	


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
			self.update_routing_table(q)

	# Routing table is a String table with a String key
	# The key is the final destination
	# The value is the link
	def send(self, packet):
		p = packet.get_type()
		if (p == DATA_PACKET_TYPE) or (p == DATA_PACKET_ACKNOWLEDGEMENT_TYPE): 
			# Current is a dict.  We are trying to get the packet destination which is the dict key
			# next_dest is a String of the link that should be sent to		
			next_dest = self.current[packet.get_dest()] # a link
			self.sim.get_element(next_dest).send(packet, self.get_id())	
			# self.log("Sent packet id %d of type %s to %s" % (packet.get_ID(), packet.get_type(), next_dest))
		elif (p == ROUTER_PACKET_TYPE):
			node = packet.get_link()
			self.sim.get_element(node).send(packet, self.get_id())
		elif (p == ROUTER_PACKET_ACKNOWLEDGEMENT_TYPE):
			# Create a cost for traveling through the link
			link = self.sim.get_element(packet.get_link())
			packet.set_cost(link.get_delay() + (link.get_rate()*link.get_occupancy()))
			link.send(packet, self.get_id())


	# dict routing_table: routing table
	# key: destination host id
	# value tuple (distance between current router and destination host,
	# next hop)
	'''
	def initalize_routing_table(self,hosts_ids):
		# Initialize routing table by creating keys for all hosts in the test case
		# The value of the table is a tuple (distance between current router and destination host, next hop)
		# Initially, set the distance to be inf, the next hop to host connected to link[0]
		for host_id in hosts_ids:
			value = float('inf'),self.links[0].dest
			self.routing_table[host_id] = value
		# If the host destination is directly connected to the router (neighbor), set the distance to 1 and next hop to the host
		for link2 in self.links:
			if # host is a neighbor (host=link2.dest)
				value = 1, # this host
				self.routing_table[host] = value
		# Send first iteration of router packet
		self.send_router_packet()

	def received_packet_type():
		# Based on the type of the received packet, call the corresponding function:
		# If the received packet type is DATA or ACK_DATA, call map_route()
		# If the received packet type is ROUTER, call send_ack_router_packet()
		# If the received packet type is ACK_ROUTER, call update_routing_table()

	def update_routing_table(self):
		# Implement Bellman-Ford algorithm
		# Compare router table from acknowledgement of router packet received from neighbor routers and the current router. 
		# Update router table if there is a shorter path.
		# Static routing: metric based on hops (1 hop for each link)
		# Dynamic routing: metric based on link delays (Update routing table based on the received router packets’ timestamps)
		for (d,v) in every item in routing table:
			if static routing:
				metric = 1
				if d in self.table:
					if v[0] + metric < self.table [d][0]:
						new_v = v[0] + metric , #host source of router packet
						self.table[d] = new_v
				else:
					new_v = v[0] + metric , #host source of router packet
					self.table[d] = new_v
			else: #dynamic routing
				meric = #link delay (timestamp now - start timestamp when router packet sent)
				if d in self.table:
					if v[0] + metric < self.table [d][0]:
						new_v = v[0] + metric , #host source of router packet
						self.table[d] = new_v
				else:
					new_v = v[0] + metric , #host source of router packet
					self.table[d] = new_v				

	def send_router_packet():
		# Send the routing table of this router to communicate with its neighbor
 		# Send router packet to their neighbors
		# Router packet creates start timestamp

	def send_ack_router_packet():
		# Send an ACK_ROUTER type packet
		# Send acknowledgement back to original router after receiving router packet
		# Acknowledgement packet contains a copy of routing table and keeps start timestamp

	def map_route():
		# Get the destination of packet, then look up current routing table, find next hop and send the packet to next link

	def routing_table_timeout():
		# Updates routing table periodically. Send ROUTER packets to all neighboring links
		# Send_router_packet()

	'''

	def set_event_simulator (self, sim):
		self.sim = sim

	def get_link(self):
		return self.link

	def get_dest (self):
		return self.dest 
