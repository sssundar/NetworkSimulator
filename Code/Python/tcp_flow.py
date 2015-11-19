# TCP Reno Flow Code

# Sith Domrongkitchaiporn

from reporter import Reporter
from packet import *
import math, constants
from events import *
from flow import *

class Data_Sink_TCP_RENO(Data_Sink):

	def __init__(self, identity, src, sink, size, start):		
		Data_Sink.__init__(self, identity, src, sink, size, start)      		

	# Acknowledge the last packet received in linear sequence.
	# E.g. receiving packets 1,2,3,5 will acknowledge 1,2,3,3
	def receive(self, packet):
		if constants.MEASUREMENT_ENABLE: 
			print constants.MEASURE_FLOWRATE((self,packet.get_kbits(),self.sim.get_current_time()))
		self.rx_buffer[packet.get_ID()] = 1

		p = None
		# Packets are indexed from 0, too.
		for i in range (0, len(self.rx_buffer)):
			if not (self.rx_buffer[i]):
				# Make new Packet
				p = Packet(self, self.source, self.dest, \
					constants.DATA_PACKET_ACKNOWLEDGEMENT_TYPE, i-1, \
					constants.DATA_ACK_BITWIDTH)
				break		
		if p is None:
			p = Packet(self, self.source, self.dest, \
					constants.DATA_PACKET_ACKNOWLEDGEMENT_TYPE, packet.get_ID(), \
					constants.DATA_ACK_BITWIDTH)
		self.send(p)


''' 
From first slow start -> go doubling on RTT. 				 	DONE
On 3-ack, to fr/ft with half congestion window 					DONE
On TO - to 1 with congestion threshold to W_max/2, W = 1 		DONE
	Wait for ~RTT_congested for outstanding to TO/ack
	Do not repeat TO W/2 for each other TO, till actually
	send new packets (outstanding < 1)

When ramping in next ss, go till threshold for congestion,		DONE
then enter CA (+1/W) directly. Should also be able to enter
fast retransmit, fast recover. 

From slow-start again, TO halves current W to new CA threshold 	DONE
and starts from w=1

From CA TO does this, always, to slow start with W/2 threshold. DONE

3-acks always to fr/ft without changing CA threshold, starting 	DONE
at W/2.

if TO in fr/ft set CA threshold to half of 'true W' at start of fr/ft   DONE
then start with W = 1

triple-acks should reach into packets and tell them they're already assumed DONE
dead, no need to time out.
'''
class Data_Source_TCP_RENO(Data_Source):
	last_three = [] 
	
	# if not in slow_start or fast_recover, are in congestion_avoidance
	fast_recover = False
	slow_start = True	
	
	# slow-start to congestion avoidance threshold
	threshold = -1 # initially "infinite"
	fr_window = 0 		# window at start of latest ft/fr

	timeout_count = 0 # count of latest string of timeouts 

	def __init__(self, identity, src, sink, size, start):
		Data_Source.__init__(self, identity, src, sink, size, start)	

		self.last_three = [-3,-2,-1]				# Last 3 ACK IDs received
		
		self.fast_recover = False 					# In the middle of packet lost?		
		self.slow_start = True		
		self.threshold = -1 		
		self.window = 1.0 							# no simulator to get current time from, here				
		self.fr_window = 0 
		self.timeout_count = 0

	def update_window (self, newsize):
		self.window = newsize
		if constants.MEASUREMENT_ENABLE: 
			print constants.MEASURE_FLOW_WINDOW_SIZE((self,self.window,self.sim.get_current_time()))

	def receive(self, p):
		''' 
		When a packet is assumed dropped/timed out we decrement this
		So if it hasn't actually left the network, our sink will acknowledge it
		eventually. 

		This check is to avoid a circumstance in which num_p_outstanding < 0
		'''				

		if self.num_packets_outstanding - 1 >= 0:
			self.num_packets_outstanding -= 1   # Decreased the number of packets there

		self.last_three.append(p.get_ID())
		self.last_three.pop(0)		

		print "\nDEBUG: packets outstanding : %d\n" % self.num_packets_outstanding

		# TODO: parser needs to be subclassed or have if statements
		# so we can run TCP RENO, FAST, or STATIC, and static/dynamic routing
		# through constants.constants		
		if (self.fast_recover is True):

			print "\nDEBUG: got to fast recover\n"
			if (p.get_ID() is not self.last_three[1]):				
				# Set packet ack and those before
				for i in xrange(0, min(p.get_ID()+1,len(self.tx_buffer))):
					q = self.tx_buffer[i]					
					if q.get_ack() == 0:						
						q.set_ack(1)
						q.set_in_transit(0)
						q.set_ack_time(self.sim.get_current_time())
						# TODO: Handle packet delay bursts (inferred acks) properly
						if constants.MEASUREMENT_ENABLE:
							print constants.MEASURE_PACKET_RTT((self,q.get_RTT(),self.sim.get_current_time()))
				# Set window to value at start of fast recover													
				self.update_window(self.fr_window)
				self.fast_recover = False
			else:
				# If by some horrible accident the ft/fr re-transmit 
				# of the original dropped packet ALSO got dropped
				# then we have to wait for timeout.
				# So timeout sets the worst-case response timescale of this TCP				
				self.update_window(self.window + 1)

		# self.last_three[2] is also p.get_ID()
		elif (self.last_three[2] is self.last_three[1]) and (self.last_three[0] is self.last_three[1]):
			print "\nDEBUG: got to packet loss (triple ack)\n"
			# A Packet was dropped
			self.update_window(max(self.window/2.0,1.0))			
			self.fr_window = self.window
			self.fast_recover = True 	# Need to recover from packet lost
			self.slow_start = False 	# Done with slow start if lost packet
			
			''' 
			The packet triple-acked is assumed dropped
			'''
			# Reach into the 'assumed dropped packet' and disable its timeout
			self.tx_buffer[p.get_ID()].set_timeout_disabled(True)

			# Create a new packet with this id in case old packet 
			# actually still in network. 
			q = Packet(self, self.source, self.dest, \
					constants.DATA_PACKET_TYPE, p.get_ID(), \
					constants.DATA_PACKET_BITWIDTH)
			self.tx_buffer[q.get_ID()] = q			
			
			if self.num_packets_outstanding - 1 >= 0:
				self.num_packets_outstanding -= 1   # Decreased the number of packets there
			self.send(self.tx_buffer[q.get_ID()]) 	# Send the (assumed) missing packet again			

			return 0		# Done with function

		elif (self.last_three[2] is self.last_three[1]):
			print "\nDEBUG: got to about to packet loss\n"
			# Only two duplicate acks so far
			# Don't increase window size
			pass

		elif (self.last_three[2] is not self.last_three[1]):
			print "\nDEBUG: got to nothing is wrong\n"
			# New Packet
			# In Congestion Avoidance, AIMD
			for i in xrange(0, min(p.get_ID()+1,len(self.tx_buffer))):
				q = self.tx_buffer[i]
				if q.get_ack() == 0:
					q.set_ack(1)
					q.set_in_transit(0)
					q.set_ack_time(self.sim.get_current_time())
					# TODO: Handle packet delay bursts (inferred acks) properly
					if constants.MEASUREMENT_ENABLE:
						print constants.MEASURE_PACKET_RTT((self,q.get_RTT(),self.sim.get_current_time()))

			if (self.slow_start is True):			
				self.update_window(self.window + 1)											
				if (self.threshold >= 0) and (self.window >= self.threshold):
					self.slow_start = False
			else:
				self.update_window(self.window + float(1.0/self.window))							

		else:
			print "\nDEBUG: got to wtf\n"

			# How did we get here?			
			self.log("TCP RENO receive error - unknown case. Dump follows: \
				last_three_packets: %s, %s, %s, \
				fast_recover_flag: %s, \
				slow_start_flag: %s" % (last_three[0], last_three[1], last_three[2], fast_recover, slow_start))		
				
		if not self.is_flow_done():         
			# Search entire buffer for the lowest packet without an ACK & not in transit
			# Send it over and break from the loop			
			for i in xrange(len(self.tx_buffer)):
				if (self.tx_buffer[i].get_ack() is 0) and (self.tx_buffer[i].get_in_transit() is 0):
					if self.num_packets_outstanding < self.window:
						self.send(self.tx_buffer[i])
					else:
						break

	# Timing out in the source
	'''
	On TO - to 1 with congestion threshold to W_max/2, W = 1 		
	Wait for ~RTT_congested for outstanding to TO/ack
	Do not repeat timeout threshold halving for each successive timeout, till actually
	send new packets (outstanding < W=1)
	'''
	def time_out(self, p):
		self.timeout_count = self.timeout_count + 1
		if self.timeout_count == 1:
			if self.fast_recover is True:
				self.threshold = max(self.fr_window/2.0,1.0)
			else:
				self.threshold = max(self.window/2.0,1.0)
		else:
			# Do not want a string of timeouts to drop us to 0 in threshold
			pass

		q = Packet(self, self.source, self.dest, \
				constants.DATA_PACKET_TYPE, p.get_ID(), \
				constants.DATA_PACKET_BITWIDTH)
		self.tx_buffer[q.get_ID()] = q
							# Telepathy! (not checked, though, for now)
		p.set_tx_time(-1)   # Set TX_Time as no longer valid
		p.set_in_transit(0) # Set in Transit as False
		
		if self.num_packets_outstanding - 1 >= 0:
			self.num_packets_outstanding -= 1   # Decreased the number of packets in network, probably
		
		self.poke_tcp()                     	# Poke TCP

	# We poke tcp on startup and on timeout. both enter slow start
	def poke_tcp(self):
		self.slow_start = True
		self.fast_recover = False		
		self.update_window(1.0)
		if (self.num_packets_outstanding < self.window):			
			if (self.get_next_packet_to_transmit() is not None):
				self.send(self.get_next_packet_to_transmit())
				self.poke_tcp()

	# Get the next Packet to send over
	# If a packet != sending or GOT ACK
	#   - Return the packet
	def get_next_packet_to_transmit(self):
		for i in xrange (0, len(self.tx_buffer)):
			# ! ( A | B ) = !A & !B
			if not (self.tx_buffer[i].get_in_transit() or self.tx_buffer[i].get_ack()):
				return self.tx_buffer[i]
		return None

	def is_flow_done(self):
		for i in range (0, len(self.tx_buffer)):
			if (self.tx_buffer[i].get_ack() is not 1):
				return 0
		self.set_is_done(1)
		return 1

	def send(self,p):
		self.timeout_count = 0
		p.set_in_transit(1)
		p.set_tx_time(self.sim.get_current_time())
		self.sim.get_element(self.source).send(p)
		self.num_packets_outstanding += 1		
		self.sim.request_event(\
			Time_Out_Packet(p, \
							self.sim.get_current_time() + constants.DATA_PACKET_TIMEOUT))
		