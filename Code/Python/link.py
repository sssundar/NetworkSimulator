'''
Link & LinkBuffer Code

Operation
	LinkBuffers are just arrays. They keep track of the byte size of their
	contents, and use that to determine whether new arrivals are dropped.

	Links have a bit of telepathy. They take on initialization their
	left and right node IDs, their rate in bits/s, their propagation delay
	in seconds, and their buffer size (for each of the left/right buffers)
	in bits.

Last Revised by Sith Domrongkitchaiporn & Sushant Sundaresh on 5 Nov 2015
'''

from reporter import Reporter
from link_buffer import LinkBuffer

# The class Link extends the class Reporter
class Link(Reporter):

	left_node = ""
	right_node = ""
	bit_rate = -1 
	prop_delay = -1
	buff_bits = -1 	
	left_buff = []
	right_buff = []
	sim = ""

	# Call Node initialization code, with the Node ID (required unique)
	# Initializes itself
	def __init__(self, identity, left, right, rate, delay, size):
		Reporter.__init__(self, identity)				
		self.left_node = left
		self.right_node = right
		self.bit_rate = int(rate)
		self.prop_delay = int(delay)
		self.buff_bits = int(size)

		self.left_buff = LinkBuffer(self.buff_bits)
		self.right_buff = LinkBuffer(self.buff_bits)

	def set_event_simulator (self, sim):
		self.sim = sim

	def get_left(self):
		return self.left_node

	def get_right(self):
		return self.right_node

	def get_rate(self):
		return self.bit_rate

	def get_delay(self):
		return self.prop_delay

	def get_buff(self):
		return self.buff_bits