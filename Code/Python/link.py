'''
Link

Operation
	Links have a bit of telepathy. They take on initialization their
	left and right node IDs, their rate in kbits/ms, their propagation delay
	in ms, and their buffer size (for each of the left/right buffers)
	in kbits.

	The link cannot act like a stoplight; we'll get large fluctuations in 
	queueing delay and our TCP algorithms will not stabilize.

	A packet in the buffer looks like (time_queued, packet). 
	The link keeps track of the number of packets in transit, which direction
	packets are currently flowing, and whether a packet is currently
	being loaded into the channel.

	Now, when we send a packet, we just queue it up and 
	ask the system to transfer_next_packet. Callbacks do the same, only
	loading callbacks reset the loading flag, and in transit callbacks
	ask a Node to receive the packet, and decrement the in transit count.
	
	Let event A = a packet is being loaded currently
	Let event B = a packet is in transit currently

	If !A & !B
		Start loading the head packet from whichever buffer has a smaller 
		head timestamp. Create a loading callback for this event. Set the
		direction.

	If !A & B
		Check the direction, and get the timestamp of both buffer heads. 
		If the source buffer of the packet in transit has another packet
		that can be loaded/propagate before the timestamp of the dest buffer,
		go ahead and load it (creating a callback). Otherwise, do nothing.

	If A & !B
		Do nothing.

	If A & B
		Do nothing.

Last Revised by Sith Domrongkitchaiporn & Sushant Sundaresh on 6 Nov 2015
'''

from reporter import Reporter
from link_buffer import LinkBuffer
from events import *
import constants
import sys

# The class Link extends the class Reporter
class Link(Reporter):

	left_node = ""
	right_node = ""
	
	capacity_kbit_per_ms = -1 
	kbits_in_each_buffer = -1 	
	ms_prop_delay = -1
	
	left_buff = []
	right_buff = []
	sim = ""

	packet_loading = False
	packets_in_flight = 0
	transmission_direction = "" # left-to-right, right-to-left
	switch_direction_flag = False

	bidirectional_queueing_delay_memory = [-1] * constants.QUEUEING_DELAY_WINDOW

	def ms_tx_delay (self, packet): 
		return (packet.get_kbits() / self.capacity_kbit_per_ms) # ms

	def ms_total_delay (self, packet): 
		return self.ms_tx_delay(packet) + self.ms_prop_delay # ms
	
	# Call Node initialization code, with the Node ID (required unique)
	# Initializes itself
	# Inputs: rate (Mbps), Delay (ms), size (KB)
	# We need to standardize units to kbit/ms, kbits, and ms
	def __init__(self, identity, left, right, rate, delay, size):
		Reporter.__init__(self, identity)				
		self.left_node = left
		self.right_node = right

		# Need to standardize units to kbit/ms, kbits, and ms		
		self.capacity_kbit_per_ms = float(rate)				# 1000 Kilobits in a Megabit, 1000 ms in a s
		self.ms_prop_delay = float(delay)					# Already standardized
		self.kbits_in_each_buffer = 8.0 * float(size) 		# 8 = conversion from BYTE to BIT, ignore 1024 vs 1000 convention

		self.left_buff = LinkBuffer(self.kbits_in_each_buffer)
		self.right_buff = LinkBuffer(self.kbits_in_each_buffer)

		self.bidirectional_queueing_delay_memory = [-1] * constants.QUEUEING_DELAY_WINDOW

	def set_event_simulator (self, sim):
		self.sim = sim
		self.left_buff.set_event_simulator(sim)
		self.left_buff.set_my_link(self)
		self.left_buff.set_my_direction(constants.LTR)
		self.right_buff.set_event_simulator(sim)
		self.right_buff.set_my_link(self)
		self.right_buff.set_my_direction(constants.RTL)

	def get_left(self):
		return self.left_node

	def get_right(self):
		return self.right_node

	def get_rate(self):
		return self.capacity_kbit_per_ms

	def get_delay(self):
		return self.ms_prop_delay

	def get_buff(self):
		return self.kbits_in_each_buffer

	# return time average of queueing delay buffer
	def get_occupancy(self):		
		'''
		for v in self.bidirectional_queueing_delay_memory:
			sys.stderr.write("QD: %0.3e\n"%v)
		'''
		return self.average_delay_buffer()

	def average_delay_buffer(self):
		delay = 0.0
		cnt = 0.0
		for v in self.bidirectional_queueing_delay_memory:
			if v >= 0:
				delay += v
				cnt += 1.0
		delay /= cnt
		return delay

	# reset packet loading, decide how to transfer_next_packet
	def packet_transmitted (self, packet):
		self.packet_loading = False		
		self.sim.request_event(\
			Handle_Packet_Propagation(packet, self.get_id(),\
			self.sim.get_current_time() + self.ms_prop_delay))
		self.packets_in_flight += 1
		self.transfer_next_packet()

	# decrement packets in flight counter, decide how to transfer_next_packet
	def packet_propagated (self):
		self.packets_in_flight -= 1
		self.transfer_next_packet()

	# load packet-to-send to the appropriate buffer, then decide how to 
	# transfer it
	def send (self, packet, sender_id):				
		notDroppedFlag = True
		if sender_id == self.left_node:			
			notDroppedFlag = self.left_buff.enqueue(packet)
			self.transfer_next_packet()
		elif sender_id == self.right_node:
			notDroppedFlag = self.right_buff.enqueue(packet)
			self.transfer_next_packet()
		else:
			raise ValueError ('Packet received by Link %s \
				from unknown Node %s' % (self.ID, sender_id) )
		
		if (not notDroppedFlag):	
			print "\nDEBUG: (in link) packets dropped : %s, packet %d\n" % (self.get_id(), packet.get_ID())
			if constants.MEASUREMENT_ENABLE: 
				print constants.MEASURE_PACKET_LOSS((packet.get_flow(),\
											packet.get_type(),\
											packet.get_ID(),\
											self.sim.get_current_time()))

	def transfer_next_packet (self):
		if (not self.packet_loading) and (self.packets_in_flight == 0):
			
			lt = self.left_buff.get_head_timestamp() \
						if self.left_buff.can_dequeue() else -1
			rt = self.right_buff.get_head_timestamp() \
						if self.right_buff.can_dequeue() else -1			
			
			if (lt >= 0) or (rt >= 0):				
				if (lt >= 0) and (rt >= 0):
					if self.switch_direction_flag:
						# there are packets on both sides,
						# and it's time to switch link direction
						self.switch_direction_flag = False
						if (self.transmission_direction == constants.LTR):
							self.transmission_direction = constants.RTL
							packet_to_transmit, queue_delay = self.right_buff.dequeue()
							packet_to_transmit.set_curr_dest(self.get_left())
						else:
							self.transmission_direction = constants.LTR
							packet_to_transmit, queue_delay = self.left_buff.dequeue()
							packet_to_transmit.set_curr_dest(self.get_right())
					elif (lt < rt):
						# Start loading Packet from head of left buffer into channel
						self.transmission_direction = constants.LTR
						packet_to_transmit, queue_delay = self.left_buff.dequeue()
						packet_to_transmit.set_curr_dest(self.get_right())
					else:
						# Start loading Packet from head of right buffer into channel
						self.transmission_direction = constants.RTL
						packet_to_transmit, queue_delay = self.right_buff.dequeue()
						packet_to_transmit.set_curr_dest(self.get_left())
				elif (lt >= 0):
					# Start loading Packet from head of left buffer into channel				
					self.transmission_direction = constants.LTR
					packet_to_transmit, queue_delay = self.left_buff.dequeue()
					packet_to_transmit.set_curr_dest(self.get_right())
				else:
					# Start loading Packet from head of right buffer into channel					
					self.transmission_direction = constants.RTL
					packet_to_transmit, queue_delay = self.right_buff.dequeue()
					packet_to_transmit.set_curr_dest(self.get_left())

				self.packet_loading = True
				completion_time = \
					self.sim.get_current_time() + self.ms_tx_delay(packet_to_transmit)
				
				self.sim.request_event(\
					Handle_Packet_Transmission(	packet_to_transmit,\
												self.get_id(),\
					 							completion_time))

				self.bidirectional_queueing_delay_memory.pop(0)
				self.bidirectional_queueing_delay_memory.append(queue_delay)
			else:
				pass

		elif (not self.packet_loading) and (self.packets_in_flight > 0):
			lt = self.left_buff.get_head_timestamp() \
				if self.left_buff.can_dequeue() else -1			
			rt = self.right_buff.get_head_timestamp() \
				if self.right_buff.can_dequeue() else -1
			self.attempt_to_transmit_in_same_direction (lt, rt)

		else:
			pass

	# lt, rt are left and right heads-of-buffer timestamps
	def attempt_to_transmit_in_same_direction (self, lt, rt):		
		# if there are any more to send in the current direction,
		# can they get there before the timestamp of the head of the
		# other buffer?
		if self.transmission_direction == constants.RTL:
			buff = self.right_buff
			curr_dest = self.get_left()
			t1 = lt
			t2 = rt
		else:
			buff = self.left_buff
			curr_dest = self.get_right()
			t1 = rt
			t2 = lt

		if t2 >= 0:	
			proposed_receive_time = self.sim.get_current_time() + \
				self.ms_total_delay(buff.see_head_packet())
			if ((t1 >= 0) and (proposed_receive_time < t1)) or (t1 < 0):	
				packet_to_transmit, queue_delay = buff.dequeue()
				packet_to_transmit.set_curr_dest(curr_dest)
				self.packet_loading = True
				completion_time = self.sim.get_current_time() + \
					self.ms_tx_delay(packet_to_transmit)
				self.sim.request_event(\
					Handle_Packet_Transmission(	packet_to_transmit,\
											self.get_id(),\
				 							completion_time))

				self.bidirectional_queueing_delay_memory.pop(0)
				self.bidirectional_queueing_delay_memory.append(queue_delay)

			else:
				self.switch_direction_flag = True