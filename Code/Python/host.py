# File: host.py
#
# Description: a host, with an associated link and flow
# 
# Initialization: 
#  Takes a string that is the unique host ID
#  Takes an array containing exactly 1 string, its link id
#
# Last Revised: 3 November 2015 by Sushant Sundaresh
# 					created

from node import Node
import constants

# The class Node extends the class Reporter
class Host(Node):

	element_type = ""
	link = ""
	flow = ""
	sim = ""

	# Call Node initialization code, with the Node ID (required unique)
	# Error handling on links length (indicates parser failure)
	def __init__(self, identity, links):
		if len(links) > 1:
			raise ValueError('Host constructed with >1 link.')
		else:			
			Node.__init__(self, identity)				
			self.element_type = constants.HOST_ELEMENT
			self.link = links[0]

	def get_element_type (self):
		return self.element_type

	def get_link (self):
		return self.link

	def set_flow (self, f):
		self.flow  = f
	
	def set_event_simulator (self, sim):
		self.sim = sim

	# Pre-Routing: Pass the packet directly to the flow, if it exists	
	# Post-Routing: Handle whether the packet is for routing or data flow
	def receive (self, packet):		
		raise AttributeError('Flows are not defined yet; how am I receiving?')

		# if (packet.get_type() == constants.DATA_PACKET_ACKNOWLEDGEMENT_TYPE) or \
		# 	(packet.get_type() == constants.DATA_PACKET_TYPE):
		# 	self.sim.get_element(self.flow).receive(packet)
	
	# Send the packet directly to the link
	def send (self, packet):			
		raise AttributeError('Flows are not defined yet; how am I sending?')
		# self.sim.get_element(self.link).send(packet, self.get_id())					
