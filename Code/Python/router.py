# File: router.py
#
# Assisted by Sith
#
# Description: a router, with associated links and flow
# route packets to destination host
# 
# Initialization: 
#  Takes a string that is the unique router ID
#  Takes an array containing arbitrary number of strings,
#		its connected links' id's
#
# Last Revised: 3 December 2015 by Sith Domrongkitchaiporn

from node import Node
from constants import *
from packet import *
from jsonparser import *
import sys

# The class Node extends the class Reporter
class Router(Node):

	IterationDoneFlag = False

	link = []
	sim = ""
	# dest = ""		# destination host

	# Routing Tables
	# - Current one
	# - a new one currently under construction  
	current = {}
	new = {}

	host_array = []
	no_change = 0

	# Call Node initialization code, with the Node ID (required unique)
	# Initializes itself
	def __init__(self, identity, links):
		Node.__init__(self, identity)				
		self.link = links
		self.current = {}	# Current Routing table
		self.new = {}		# Routing table under construction	
		self.itr = 0
		self.host_array = []
		self.no_change = 0

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
		'''
		sys.stderr.write("\nDEBUG ROUTER RECEIVE NEW TABLE\n")
		sys.stderr.write("%s: %s\n"%(self.get_id(), packet.get_type()))

		for (d, v) in packet.get_routing_map().items():
			sys.stderr.write("%s: %s, %0.3e, %s\n"%(self.get_id(), d,v[0],v[1]))
		'''
		p = packet.get_type()
		if (p == DATA_PACKET_TYPE) or (p == DATA_PACKET_ACKNOWLEDGEMENT_TYPE):
			self.send(packet)
		elif (p == ROUTER_PACKET_TYPE):		# Create an ACK packet and send back routing info
			link = packet.get_link()
			q = Router_Packet(ROUTER_FLOW, self.get_id(), packet.get_source(), ROUTER_PACKET_ACKNOWLEDGEMENT_TYPE, ROUTER_FLOW, DATA_ROUTER_ACK_BITWIDTH, link)
			q.set_routing_map(self.new)
			self.send(q)
		elif (p == ROUTER_PACKET_ACKNOWLEDGEMENT_TYPE):
			self.update_routing_table(packet)	# check argument q

	# Routing table is a String table with a String key
	# The key is the final destination
	# The value is the link
	def send(self, packet):
		'''
		sys.stderr.write("\nDEBUG ROUTER SEND NEW TABLE\n")
		for (d, v) in self.new.items():
			sys.stderr.write("%s: %s, %0.3e, %s\n"%(self.get_id(), d,v[0],v[1]))
		'''
		p = packet.get_type()
		if (p == DATA_PACKET_TYPE) or (p == DATA_PACKET_ACKNOWLEDGEMENT_TYPE): 
			# Current is a dict.  We are trying to get the packet destination which is the dict key
			# next_dest is a String of the link that should be sent to		
			next_dest = self.current[packet.get_dest()][1] # a link
			self.sim.get_element(next_dest).send(packet, self.get_id())	
			#sys.stderr.write("%s sending: %s to %s with dest: %s\n"%(self.get_id(), p, next_dest, packet.get_dest()))
			# self.log("Sent packet id %d of type %s to %s" % (packet.get_ID(), packet.get_type(), next_dest))
		elif (p == ROUTER_PACKET_TYPE):
			link = self.sim.get_element(packet.get_link())
			link.send(packet, self.get_id())
		elif (p == ROUTER_PACKET_ACKNOWLEDGEMENT_TYPE):
			# Create a cost for traveling through the link
			link = self.sim.get_element(packet.get_link())
			packet.set_cost(link.get_delay() + link.get_occupancy())
			link.send(packet, self.get_id())

	# Initialize routing table by creating keys for all hosts in the test case
	# The value of the table is a tuple (distance between current router and destination host, next hop(link))
	# Initially, set the distance to be inf, the next hop to link[0]
	# host_ids is an array contains all host ids

	# if routing does not converge before a new run, we toss the table. it's possible routing might not have converged
	# from the previous cycle. this will toss the intermediate table, and is a known bug.
	def initalize_routing_table(self):
		self.no_change = 0		
		self.new = {}
		self.IterationDoneFlag = False
		for host_id in self.host_array:
			value = float('inf'),self.link[0] # a default link
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
	def update_routing_table(self, router_packet):		
		for (d,v) in router_packet.get_routing_map().items(): # every item in routing table
			metric = router_packet.get_cost() #link cost
			if v[0] + metric < self.new [d][0]:
					recv_map = router_packet.get_routing_map()
					new_v = v[0] + metric , router_packet.get_link() 
					self.new[d] = new_v
					self.no_change = 0
			else:
				self.no_change = self.no_change + 1

		# Send next iteration of router packet
		if (self.no_change <= len(self.link) + len(self.new)):			
			sink = router_packet.get_source()
			packet = Router_Packet(ROUTER_FLOW,self.get_id(),sink,ROUTER_PACKET_TYPE,ROUTER_FLOW,DATA_ROUTER_BITWIDTH,router_packet.get_link())
			self.send(packet)
		else:							
			self.current = self.new	
			if not self.IterationDoneFlag:				
				'''
				sys.stderr.write("\nROUTING TABLE for %s\n"%self.get_id())
				for (d, v) in self.new.items():
					sys.stderr.write("%s, %0.3e, %s\n"%(d,v[0],v[1]))
				'''
				self.IterationDoneFlag = True

			
	def routing_table_periodic_update(self):		
		self.initalize_routing_table()

	def set_host_array(self, array):
		self.host_array = array

	def set_event_simulator (self, sim):
		self.sim = sim

	def get_link(self):
		return self.link

	def get_dest (self):
		return self.dest 
