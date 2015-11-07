# Flow Code
# Includes sub-class Data_Source

# Sith Domrongkitchaiporn
# Sushant Sundaresh

from reporter import Reporter
from packet import *

# This class only extends Reporter Class
class Flow(Reporter):
	source = ""
	dest = ""
	size = -1
	start =  -1
	sim = "" # should be set to an event_simulator object before any action
	am_i_done = 0

	# Call Node initialization code, with the Node ID (required unique)
	# Initializes itself
	def __init__(self, identity, src, sink, size, start):
		Reporter.__init__(self, identity)
		self.source = src
		self.dest = sink
		self.size = int(size)
		self.start = int(start)
		self.am_i_done = 0

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

	def is_done (self):
		return self.am_i_done

class Data_Source(Flow):
	tx_buffer = []
	num_pack_outstanding = -1

	def __init__(self, identity, src, sink, size, start):
		Flow.__init__(self, identity, src, sink, size, start)

	def get_flow_size(self):
		return len(tx_buffer)

	def send(self, p):
		p.flag_in_transit(1)
		p.set_tx_time(self.sim.get_current_time())
		self.source.send(p)
		self.num_pack_outstanding += 1

	def set_flow_size(self, bits):
		total = math.ceil(float(bits)/constants.DATA_PACKET_BITWIDTH)
		self.num_packets_outstanding = 0

		for i in range(0,total_packets - 1):
			self.tx_buffer[i] = Packet(self, self.source, self.dest, constants.DATA_PACKET_TYPE, i, constants.DATA_PACKET_BITWIDTH)

	def receive(self):
		



		


