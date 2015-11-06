class LinkBuffer:

	queued = []
	bit_capacity = 0
	current_bits_in_queue = 0

	def __init__(self, bit_capacity):
		self.bit_capacity = bit_capacity
		self.current_bits_in_queue = 0
		queued = []

	def can_enqueue (self, packet):
		if self.current_bits_in_queue + packet.get_bits() <= self.bit_capacity:
			return True
		return False 

	def enqueue (self, packet):
		if self.can_enqueue(packet):
			self.queued.append(packet)
			self.current_bits_in_queue += packet.get_bits()
			return True
		return False # packet dropped

	def can_dequeue (self):
		if length(self.queued) > 0:
			return True
		return False

	# You must call this function after checking can_dequeue; otherwise
	# the return value is not guaranteed to be a packet
	def dequeue (self):
		if self.can_dequeue():
			p = self.queued.pop(0)
			self.current_bits_in_queue -= p.get_bits()
			return p