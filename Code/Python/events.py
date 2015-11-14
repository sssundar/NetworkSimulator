'''
Events
	A collection of events to, for example
		handle packet propagation delay
		handle packet transmission delay
		handle packet time outs
		handle flow start 

Last Revised: 
	06 Nov 2015, Sushant Sundaresh, created
'''

from event import Event
import constants

class Handle_Packet_Propagation (Event):
	p = "" 	# Packet Propagating to a Node (Router/Host)
	l = "" 	# The link ID it's propagating on

	def __init__ (self, packet, link, completion_time):
		self.p = packet
		self.l = link
		self.set_completion_time(completion_time)
	
	def event_action (self, sim):		
		if constants.MEASUREMENT_ENABLE:
			print constants.MEASURE_LINKRATE((sim.get_element(self.l),\
											self.p.get_kbits(),\
											self.get_completion_time()))
		sim.get_element(self.l).packet_propagated()
		sim.get_element(self.p.get_curr_dest()).receive(self.p)
	
class Time_Out_Packet (Event):
	p = "" 		# Packet to Time Out
	
	def __init__ (self, packet, completion_time):
		self.p = packet
		self.set_completion_time(completion_time)
	
	def event_action (self, sim):
		if not self.p.get_ack():
			self.p.get_flow().time_out(self.p)
			# ask the flow source to TO the packet

class Handle_Packet_Transmission (Event):
	p = "" 	# the packet being transmitted into the channel
	l = ""	# Link ID
			# This link needs to know this packet
			# has now been transmitted into the channel, and is now
			# propagating down the channel
			# It must remove this packet from its buffer 

	def __init__ (self, packet, link, completion_time):
		self.l = link		
		self.p = packet
		self.set_completion_time(completion_time)

	def event_action (self, sim):
		sim.get_element(self.l).packet_transmitted(self.p)		

class Flow_Start (Event):
	f = ""  # the flow ID to start

	def __init__ (self, ID, completion_time):
		self.f = ID
		self.set_completion_time(completion_time)

	def event_action (self, sim):
		sim.get_element(self.f).start()