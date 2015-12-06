'''
Train Link (doesn't stoplight packets as much)
Extends Link

Operation
	Our old Link tended to act like a stoplight because it required
	a packet to be able to make it to the other side before it'd send it,
	if there was already something queued on the other end (i.e. not possible)

	This revision allows packets to transmit so long as their timestamp
	beats the other guy (in the opposite buffer). So we expect packet trains.

Last Revised by Sushant Sundaresh on 6 Nov 2015
'''

from link import Link
import constants
from events import *
import sys

class Train_Link(Link):

	def __init__(self, identity, left, right, rate, delay, size):
		Link.__init__(self, identity, left, right, rate, delay, size)

	# lt, rt are left and right heads-of-buffer timestamps
	# they are -1 if the buffer is empty, and positive (or zero) otherwise
	def attempt_to_transmit_in_same_direction (self, lt, rt):		
		# if there are any more to send in the current direction,
		# do they have a smaller timestamp than whatever is at the head of
		# the other buffer?

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
	
		if (t2 <= t1) and (t2 >= 0):
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
		elif (t1 >= 0):			
			self.switch_direction_flag = True