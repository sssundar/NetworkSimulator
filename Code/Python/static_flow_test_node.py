# File: static_flow_test_node.py
#
# Description: two fake nodes to help us test static data flow sources & sinks

from node import Node

class Static_Data_Source_Test_Node(Node):
	
	tx_buff = [] # came from flow, contains packets
	f = "" 	# my associated flow id

	def __init__(self, ID, flow):
		Node.__init__(self, ID)				
		self.f = flow
	
	# returns packet ids
	def head_of_tx_buff (self):
		if len(self.tx_buff) > 0:
			return self.tx_buff.pop(0).get_ID()
		else:
			raise ValueError("Nothing left in tx buffer")

	# received from imaginary link
	def receive (self, packet):
		self.sim.get_element(self.f).receive(packet)

	# sent by our associated flow
	def send (self, packet):
		self.tx_buff.append(packet)

'''
For now, static sink test nodes do exactly what static source nodes do.
'''
class Static_Data_Sink_Test_Node(Static_Data_Source_Test_Node):
	
	def __init__(self, ID, flow):
		Static_Data_Source_Test_Node.__init__(self, ID, flow)						
	