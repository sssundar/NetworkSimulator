'''
	LinkBuffers are just arrays. They keep track of the kbit size of their
	contents, and use that to determine whether new arrivals are dropped.
'''

from constants import *
import sys

class LinkBuffer:

	mylink = ""			# object pointer, not string
	mydirection = "" 	# see constants RTL, LTR
	queued = []
	kbit_capacity = 0.0
	current_kbits_in_queue = 0.0
	sim = "" # event simulator

	def __init__(self, kbit_capacity):		
		self.kbit_capacity = kbit_capacity
		self.current_kbits_in_queue = 0.0
		self.queued = []		

	def set_event_simulator (self, sim):
		self.sim = sim

	def get_fractional_occupancy (self):
		return self.current_kbits_in_queue / self.kbit_capacity

	def get_num_queued(self):
		return len(self.queued)

	# link object pointer & buffer direction, for consolidated logging in 
	# buffers themselves
	def set_my_link (self, link):
		self.mylink = link

	def set_my_direction (self, direction):
		self.mydirection = direction

	def get_head_timestamp (self):
		return self.queued[0][0]

	def see_head_packet (self):
		return self.queued[0][1]
	

	'''
	If Packet type is Routing related, it has priority and goes to the top of queue.
	'''
	def can_enqueue (self, packet):
		p = packet.get_type()

		if (p == ROUTER_PACKET_TYPE) or (p == ROUTER_PACKET_ACKNOWLEDGEMENT_TYPE):			
			while self.current_kbits_in_queue + packet.get_kbits() > self.kbit_capacity:				
				unjustlyDroppedBySith = self.queued.pop()
				self.current_kbits_in_queue -= unjustlyDroppedBySith[1].get_kbits()				
			return True
		elif self.current_kbits_in_queue + packet.get_kbits() <= self.kbit_capacity:
			return True
		return False 

	def enqueue (self, packet):

		if self.can_enqueue(packet):
			p = packet.get_type()
			if (p == ROUTER_PACKET_TYPE) or (p == ROUTER_PACKET_ACKNOWLEDGEMENT_TYPE):								
				# so think of our routing algorithm as "I'll give my routing packets priority,
				# but before I do, I'll let the other side of the link finish transmitting, and
				# when I see a break, I'll send it through." 
				self.queued.insert(0, [self.sim.get_current_time(), packet])
				
				# the following might make routing fail to converge in time for large networks				
				# it also destabilizes TCP for test case 2. we're not sure why.				
				#self.queued.append([self.sim.get_current_time(), packet])
			else:
				self.queued.append([self.sim.get_current_time(), packet])
			
			self.current_kbits_in_queue += packet.get_kbits()

			if MEASUREMENT_ENABLE: 
				#sys.stderr.write("SITH: %s,%s,%s,%s,%s, %s\n"%(self.mylink.get_id(),p,packet.get_source(),packet.get_dest(),packet.get_curr_dest(), packet.get_ID()))

				print MEASURE_BUFFER_OCCUPANCY(\
					(self.mylink,\
					self.mydirection,\
					self.get_fractional_occupancy(),\
					self.sim.get_current_time()))
				
			return True
		return False # packet dropped

	def can_dequeue (self):
		if len(self.queued) > 0:
			return True
		return False

	# You must call this function after checking can_dequeue; otherwise
	# the return value is not guaranteed to be a packet
	# if successful, returns packet and queuing delay
	def dequeue (self):
		if self.can_dequeue():
			time_queued, p = self.queued.pop(0)
			self.current_kbits_in_queue -= p.get_kbits()

			if MEASUREMENT_ENABLE: 
				print MEASURE_BUFFER_OCCUPANCY(\
					(self.mylink,\
					self.mydirection,\
					self.get_fractional_occupancy(),\
					self.sim.get_current_time()))

			return (p, self.sim.get_current_time() - time_queued)
		else:
			raise ValueError('Dequeue violated. No packet in buffer.')