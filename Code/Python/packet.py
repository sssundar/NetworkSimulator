# Packet Code
# Sith Domrongkitchaiporn

class Packet:

	flow = "" 		# associated flow source object
	source = "" 	# original source id string
	dest = "" 		# final destination id string
	curr_dest = "" 	# intermediate destination id (next hop)
	typ = "" 		# Data, Ack, Routing.. 
	ID = -1 		# Packet ID in its flow, or Ack ID (next in sequence?)
	kbits = -1      # How big the packet is
	ack = 0         # Boolean (Has it been acknowledged)
	in_transit = 0  # Boolean
	tx_time = -1    # ms
	ack_time = -1 	# ms 	
	timeout_disabled = False

	# Initializes itself
	def __init__(self,flow,src,sink,typ,ID,kbits):
		self.flow = flow              
		self.source = src
		self.dest = sink
		self.typ = typ
		self.ID = ID
		self.kbits = kbits
		self.timeout_disabled = False

	def get_timeout_disabled (self):
		return self.timeout_disabled
		
	def set_timeout_disabled (self,val):
		self.timeout_disabled = val

	def get_flow(self):
		return self.flow

	def get_source(self):
		return self.source

	def get_dest(self):
		return self.dest

	def get_curr_dest(self):
		return self.curr_dest
	
	def set_curr_dest(self, d):
		self.curr_dest = d

	def get_type(self):
		return self.typ

	def get_ID(self):
		return self.ID

	def get_kbits(self):
		return self.kbits

	def get_ack(self): 
		return self.ack

	def get_in_transit(self):
		return self.in_transit

	def get_tx_time(self):
		return self.tx_time

	def get_ack_time(self):
		return self.ack_time

	# Get Round Trip Time
	# If ack time is NOT invalid
	# 	- return ack time - tx time
	# Otherwise, return -1
	def get_RTT(self):
		t = -1
		if (self.ack_time is not -1):
			t = self.ack_time - self.tx_time
		return t

	def set_ack(self, flag):
		self.ack = flag

	def set_in_transit(self, flag):
		self.in_transit = flag

	def set_tx_time(self, time):
		self.tx_time = time

	def set_ack_time(self, time):
		self.ack_time = time

''' 
Router_Packets extends Packets
- used by routers to request and send routing table 
- For Bellman-Ford
''' 
class Router_Packet(Packet):
	routing_map = {}	# Storage for routing table
	cost = 0
	using_link = ""		# String (which link was used to communicate)

	# Calls Flow class to init
	def __init__(self,flow,src,sink,typ,ID,kbits,link):
		self.routing_map = {}
		Packet.__init__(self,flow,src,sink,typ,ID,kbits)
		self.set_timeout_disabled(True)
		self.cost = 0
		self.using_link = link

	def set_routing_map(self, table):
		self.routing_map = table

	def get_routing_map(self):
		return self.routing_map

	def set_cost(self, value):
		self.cost = value

	def get_cost(self):
		return self.cost

	def get_link(self):
		return self.using_link