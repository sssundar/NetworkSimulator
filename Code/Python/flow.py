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
	window = 2

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
	num_packets_outstanding = -1

	def __init__(self, identity, src, sink, size, start):
		Flow.__init__(self, identity, src, sink, size, start)

	def get_flow_size(self):
		return len(self.tx_buffer)

	def send(self, p):
		p.flag_in_transit(1)
		p.set_tx_time(self.sim.get_current_time())
		self.sim.get_element(self.source).send(p)
		self.num_packets_outstanding += 1

	def set_flow_size(self, bits):
		total = math.ceil(float(bits)/constants.DATA_PACKET_BITWIDTH)
		self.num_packets_outstanding = 0

		for i in range(0,total_packets):
			self.tx_buffer[i] = Packet(self, self.source, self.dest, constants.DATA_PACKET_TYPE, i, constants.DATA_PACKET_BITWIDTH)

	def receive(self, p):
		self.tx_buffer[p.get_ID - 1].set_ack(1)

		for i in range(0, len(self.tx_buffer)):
			if (self.tx_buffer[i].get_ack() is 0):
				self.send(self.tx_buffer[i])
				break

	def start():
		poke_tcp()

	def time_out(self, p):
		p.set_tx_time(-1)
		p.set_in_transit(0)	# Set in Transit as False
		self.num_packets_outstanding -= 1
		poke_tcp()

	def poke_tcp(self):
		if (self.num_packets_outstanding < self.window):
			send(get_next_packet_to_transmit())
		poke_tcp()

	def get_next_packet_to_transmit():
		for i in range (0, len(self.tx_buffer)):
			if not (self.tx_buffer[i].is_in_transit() or self.tx_buffer[i].get_ack()):
				return self.tx_buffer[i]

class DataSink(Flow):
	rx_buffer[]

	def __init__(self, identity, src, sink, size, start):
		Flow.__init__(self, identity, src, sink, size, start)
		
	def set_flow_size(num_packets):
		for i in range (num_packets):
			self.rx_buffer[i] = 0

	def send(packet):
		p.set_tx_time(self.sim.get_current_time())
		p.set_in_transit(1)
		self.source.send(p)
