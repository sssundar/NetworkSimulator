'''
	LinkBuffers are just arrays. They keep track of the kbit size of their
	contents, and use that to determine whether new arrivals are dropped.
'''

import constants

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
		
	def can_enqueue (self, packet):
		if self.current_kbits_in_queue + packet.get_kbits() <= self.kbit_capacity:
			return True
		return False 

	def enqueue (self, packet):
		if self.can_enqueue(packet):
			self.queued.append([self.sim.get_current_time(), packet])
			self.current_kbits_in_queue += packet.get_kbits()

			if constants.MEASUREMENT_ENABLE: 
				print constants.MEASURE_BUFFER_OCCUPANCY(\
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
	def dequeue (self):
		if self.can_dequeue():
			time_queued, p = self.queued.pop(0)
			self.current_kbits_in_queue -= p.get_kbits()

			if constants.MEASUREMENT_ENABLE: 
				print constants.MEASURE_BUFFER_OCCUPANCY(\
					(self.mylink,\
					self.mydirection,\
					self.get_fractional_occupancy(),\
					self.sim.get_current_time()))

			return p
		else:
			raise ValueError('Dequeue violated. No packet in buffer.')