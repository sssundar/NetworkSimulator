# File: static_flow_test_node.py
#
# Description: two fake nodes to help us test static data flow sources & sinks

from node import Node

class Static_Data_Source_Test_Node(Node):
	
	tx_buff = [] # came from flow
	f = "" 	# my associated flow

	def __init__(self, ID, flow):
		Node.__init__(self, ID)				
		self.f = flow
	
	def last_sent_packet_id (self):
		return self.tx_buff.pop()

	# received from imaginary link
	def receive (self, packet):
		self.f.receive(packet)

	# sent by our associated flow
	def send (self, packet):
		self.tx_buff.append(packet.get_id())