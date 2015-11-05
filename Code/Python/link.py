'''
Link Code

Operation
	

Last Revised by Sith Domrongkitchaiporn & Sushant Sundaresh on 4 Nov 2015
'''

from reporter import Reporter

# The class Link extends the class Reporter
class Link(Reporter):

	left = ""
	right = ""
	rate = -1 
	delay = -1
	buff = -1
	left_buff = []
	right_buff = []
	sim = ""

	# Call Node initialization code, with the Node ID (required unique)
	# Initializes itself
	def __init__(self, identity, left, right, rate, delay, size):
		Reporter.__init__(self, identity)				
		self.left = left
		self.right = right
		self.rate = int(rate)
		self.delay = int(delay)
		self.buff = int(size)

	def set_event_simulator (self, sim):
		self.sim = sim

	def get_left(self):
		return self.left

	def get_right(self):
		return self.right

	def get_rate(self):
		return self.rate

	def get_delay(self):
		return self.delay

	def get_buff(self):
		return self.buff