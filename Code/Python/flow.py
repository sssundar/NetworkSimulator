# Flow Code
# Includes sub-class Data_Source/Data_Sink

# Sith Domrongkitchaiporn
# Sushant Sundaresh

from reporter import Reporter
from packet import *
import math, constants

# This class only extends Reporter Class
class Flow(Reporter):
	source = ""		# String
	dest = ""		# String
	size = -1		# float
	start_time =  -1 	# float
	sim = "" # should be set to an event_simulator object before any action
	am_i_done = 0	# Boolean
	window = 2		# float (window size) 

	# Call Node initialization code, with unique ID
	# Input are all Strings
	def __init__(self, identity, src, sink, amount, start):
		Reporter.__init__(self, identity)
		self.source = src
		self.dest = sink
		self.size = float(amount * 8000)
		self.start_time = float(start * 1000)		# 1000ms in a second
		self.am_i_done = 0

	# Set itself a simulator object
	def set_event_simulator (self, sim):
		self.sim = sim

	def get_source (self):
		return self.source

	def get_dest (self):
		return self.dest  

	def get_size (self):
		return self.size  

	def get_start (self):
		return self.start_time

	# Check to see if done
	def is_done (self):
		return self.am_i_done


# Extends Flow class
# Used by the Flow Source
class Data_Source(Flow):
	tx_buffer = ""		# Array for storing Packets
	num_packets_outstanding = 0	

	# Calls Flow class to init
	def __init__(self, identity, src, sink, size, start):
		self.tx_buffer = []		
		Flow.__init__(self, identity, src, sink, size, start)
		self.set_flow_size(size)

	# size in packets
	def get_flow_size(self): 
		return len(self.tx_buffer)

	# Send Packets
	# Set a flag in packet as transmitting
	# Set Tx Time
	# Initiate the source to send the packet over
	#	- Requires sim to do look Hash Table look up
	# In crease the number of packets remaining
	def send(self, p):
		p.set_in_transit(1)
		p.set_tx_time(self.sim.get_current_time())
		self.sim.get_element(self.source).send(p)
		self.num_packets_outstanding += 1

	# Set Flow Size
	# Use calculatied formula
	def set_flow_size(self, kilobits):
		total = int(math.ceil(float(kilobits)/constants.DATA_PACKET_BITWIDTH))
		self.num_packets_outstanding = 0

		# Create Packets in the buffer so that it's read to be sent
		# Packet number starts at 0		
		for i in range(0,total):
			self.tx_buffer.append(Packet(self, self.source, self.dest, constants.DATA_PACKET_TYPE, i, constants.DATA_PACKET_BITWIDTH))			

	# Read ACK packet ID and set the Acknowledgement are received even if already Timed out
	# Check for the lowest value ID without an ACK and CALL send()
	def receive(self, p):
		self.tx_buffer[p.get_ID()].set_ack(1)
		self.num_packets_outstanding -= 1	# Decreased the number of packets there

		# Search entire buffer for the lowest packet without an ACK
		# Send it over and break from the loop
		for i in range(0, len(self.tx_buffer)):
			if (self.tx_buffer[i].get_ack() is 0) and (self.tx_buffer[i].get_in_transit() is 0):
				self.send(self.tx_buffer[i])
				break

	# Poking TCP
	def start(self):
		self.poke_tcp()

	# Timing out in the source
	def time_out(self, p):
		p.set_tx_time(-1)	# Set TX_Time as no longer valid
		p.set_in_transit(0)	# Set in Transit as False
		self.num_packets_outstanding -= 1	# Decreased the number of packets there
		self.poke_tcp()						# Poke TCP

	# When the window size is bigger than packets outstanding
	# Start sending the next one.
	# re Poke TCP
	def poke_tcp(self):
		if (self.num_packets_outstanding < self.window) and \
			(self.get_next_packet_to_transmit() is not None):
			self.send(self.get_next_packet_to_transmit())
			self.poke_tcp()

	# Get the next Packet to send over
	# If a packet != sending or GOT ACK
	#	- Return the packet
	def get_next_packet_to_transmit(self):
		for i in range (0, len(self.tx_buffer)):
			# ! ( A | B ) = !A & !B
			if not (self.tx_buffer[i].get_in_transit() or self.tx_buffer[i].get_ack()):
				return self.tx_buffer[i]
		return None

# Extends Flow class
# Used by the Flow Destination
# Deal mostly with receiving and sending ACKs
class Data_Sink(Flow):
	rx_buffer = ""	# A boolean array

	# Calls flow class to init
 	# Start is irrelevant here, sinks can be started immediately. 
 	# Size is irrelevant here too, the parser will call set_flow_size
 	# once it creates the source & asks it to calculate the packet count
	def __init__(self, identity, src, sink, size, start):
		self.rx_buffer = []
		Flow.__init__(self, identity, src, sink, size, start)		

	# Init array so the Rx for each packet = FALSE
	# This must be done by the parser (telepathy)
	def set_flow_size(self, num_packets):
		self.rx_buffer = [0] * num_packets

	# Send Function
	# Set Tx_time
	# Set Packet as In_Transit
	# Make the source send it over
	#	- Find the source object via hash table in Simulator
	def send(self, packet):
		packet.set_tx_time(self.sim.get_current_time())
		packet.set_in_transit(1)
		self.sim.get_element(self.source).send(packet)

	# Destination receiving
	# Set the RX buffer for that ID as Received
	# Create an ACK packet to send back
	# Call the send function to send it over
	def receive(self, packet):
		self.rx_buffer[packet.get_ID()] = 1
		p = Packet(self, self.source, self.dest, \
			constants.DATA_PACKET_ACKNOWLEDGEMENT_TYPE, packet.get_ID(), \
			constants.DATA_ACK_BITWIDTH)
		self.send(p)
