'''
# TCP Reno Flow Sink - Specification
# Last Revised 
#	by Sushant Sundaresh on 30 November 2015
# 		Modified Slightly

	receive(self, p):
		when creating ack packet, include timestamp from p
'''

from reporter import Reporter
from packet import *
import math
from constants import *
from events import *
from flow import *
import sys

class Working_Data_Sink_TCP_RENO(Data_Sink):

	def __init__(self, identity, src, sink, size, start):		
		Data_Sink.__init__(self, identity, src, sink, size, start)      		
	
	# Do not set Tx_time (see receive)
	# Set Packet as In_Transit	
	def send(self, packet):		
		packet.set_in_transit(1)
		self.sim.get_element(self.source).send(packet)
	
	# Acknowledge the last packet received in linear sequence.
	# E.g. receiving packets 1,2,3,5 will acknowledge 1,2,3,3
	def receive(self, packet):		
		if constants.MEASUREMENT_ENABLE: 
			print constants.MEASURE_FLOWRATE((self,packet.get_kbits(),self.sim.get_current_time()))
		# There's a chance that RENO will break.
		send_flag = 1
		if (self.rx_buffer[packet.get_ID()] == 0):
			send_flag = 1

		self.rx_buffer[packet.get_ID()] = 1		
		p = None		
		for i in xrange(len(self.rx_buffer)):
			if not (self.rx_buffer[i]):				
				p = Packet(self, self.source, self.dest, \
					constants.DATA_PACKET_ACKNOWLEDGEMENT_TYPE, i-1, \
					constants.DATA_ACK_BITWIDTH)
				break		
		if p is None:			
			p = Packet(self, self.source, self.dest, \
					constants.DATA_PACKET_ACKNOWLEDGEMENT_TYPE, packet.get_ID(), \
					constants.DATA_ACK_BITWIDTH)		
		
		# ack using tx_time from p
		p.set_tx_time(packet.get_tx_time())

		if (send_flag):
			self.send(p)


''' 
# TCP Reno Flow Source - Specification
# Last Revised 
#	by Sushant Sundaresh on 30 November 2015
# 		Gutted, Restructured

This flow keeps track of:
	EPIT: estimated packets in transit
	
	In a Tx_Buffer, all Packets, with Packet State Referencing
		Case PSUA: packet sent but unacknowledged
		Case PSAA: packet sent and acknowledged
		Case PUUA: packet unsent and unacknowledged

	LPIA: last packet id acknowledged

	WS: window size
	CAT: congestion avoidance threshold from slow start (only changed on timeout)
	STT: send-time threshold 
	L3P: last three packet ids

	Flags
		TAF triple ack 
		DAF double ack
		SAF single ack 

	States
		SS, slow start (WS+=1)
		CA, congestion avoidance (WS+=1/WS)
		FR, fast retransmit, fast recover (WS+=1)		
		TR, timeout recovery

Operation	
	# Packets will be sent out with a timestamp local to the machine.
	# This will be preserved in the Ack packet.		
	send(self, packet):
		other than setting timestamp, exactly our old send
	
	# We set the STT on timeouts to avoid responding to packets that we 
	# thought were timed out.
	timeout(self, packet):
		if packet.timeout_enabled():
			EPIT = max(EPIT-1,0)
			Replace the packet that timed out with a fresh one

			if State != TR:
				State = TR
				STT = self.sim.get_current_time()
				CAT = WS/2 				# NOT CAT/2
				L3P = [-3, -2, -1]			
				WS = 1
			elif EPIT < WS:
				State = SS
				transmit()

	# called on the first recognition of a triple-ack	
	setup_fr(self):
		disables timeout on the packet triple acked in L3P
		creates a new packet with that id		
		EPIT = max(EPIT-1,0)		

	# From WS & EPIT & Tx_Buffer, determines how many packets to send	
	transmit(self):		
		for m in xrange(len(Tx_Buffer)):
			if EPIT < WS:
				if not (Tx_Buffer[m].get_in_transit() or Tx_Buffer[m].get_ackd()):
					send(Tx_Buffer[m])
			else:
				break			

	# log all state 
	debug_log_reno_source(self):
		EPIT
		LPIA
		WS
		CAT
		STT
		L3P[0,1,2]
		TAF,DAF,SAF = 0/1
		State (1,2,3,4 = SS, CA, FR, TR)

	# initialization from event simulator
	start(self):
		WS = 1
		EPIT = 0
		STT = self.sim.get_current_time()
		L3P = [-3, -2, -1]				
		LPIA = -1
		CAT = -1
		State = SS
		transmit()

	receive(self, packet):
		NAC = 0
		If Packet ID > LPIA:			
			Set acks up to Ack packet ID if needed
				Set RTT for those packets 
				Reset in transit for those packets
				if State != TR:
					at the same time as you reset in transit, 
					Set ignore timeout flags in packets up to Ack packet ID
			Set NAC to how many new Acks were set
			LPIA = Packet ID

		# When we check Ack packets, we'll use them to make next-Packet decisions,
		# but only use them to update state (i.e. as a measure of congestion)
		# if their timestamp is greater than our STT.				
		# Checking >= STT forces us, in TR, to wait for the timeout of every packet in our window
		# somewhat clearing our congestion from the network, before starting again
		# also ensures we don't respond to acks from previous timeout cycles in our current CC
		If timestamp >= STT:
			EPIT = EPIT-NAC if EPIT-NAC >= 0 else 0
			Update 3-deep Ack Memory 
			Set TAF,DAF,SAF flags					
			# on TO reset 3-deep Ack memory

		Choose current state based on previous state, WS, and 3-Ack memory
			if State = TR:
				State = TR
			elif State = SS:				
				if SAF:
					if CAT < 0 or WS < CAT:
						State = SS
					else:						
						State = CA
				elif DAF:
					State = SS
				elif TAF:	
					WS /= 2	
					CAT = WS
					setup_fr()
					State = FR		
				else:
					raise ValueError
			elif State = CR:
				if SAF:
					State = CA
				elif DAF:
					State = CA
				elif TAF:
					WS /= 2
					setup_fr()
					State = FR
				else:
					raise ValueError
			elif State = FR:
				if SAF:
					WS /= 2
					State = CA
				elif TAF:
					State = FR
				else:
					raise ValueError
			else:
				raise ValueError

		Operate from current state
			if State = TR:
				# do nothing, wait for all to time out, even if received some
				# insofar as is possible want to clear our congestion				
				pass
			else:
				if State = SS:	
					WS += 1								
				elif State = CR:
					WS += 1/WS					
				elif State = FR:						
					WS += 1					
				else:
					raise ValueError
				transmit()
'''
class Working_Data_Source_TCP_RENO(Data_Source):
	EPIT = 0 # estimated packets in transit

	LPIA = -1 # last packet id acknowledged

	WS = 0.0 # window size
	CAT = -1.0 # congestion avoidance threshold from slow start (only changed on timeout)
	STT = 0.0 # send-time threshold 
	L3P = [-3, -2, -1] # last three packet ids

	TAF = False #	TAF triple ack 
	DAF = False #	DAF double ack
	SAF = False #	SAF single ack 

	updateCount = FAST_UPDATE_PERCENTAGE_DELAY

	RTTactBuff = [-1] * constants.FAST_RTT_WINDOW_SIZE
	RTTactEst = -1	

	State = SS
	# constants.SS,CA,FR,TR
	# States
	# 	SS, slow start (WS+=1)
	# 	CA, congestion avoidance (WS+=1/WS)
	# 	FR, fast retransmit, fast recover (WS+=1)		
	# 	TR, timeout recovery

	def __init__(self, identity, src, sink, size, start):
		Data_Source.__init__(self, identity, src, sink, size, start)	
		
		RTTactBuff = [-1] * constants.FAST_RTT_WINDOW_SIZE
		RTTactEst = -1	

		self.EPIT, self.LPIA, self.WS,\
		self.CAT, self.STT, self.L3P,\
		self.TAF, self.DAF, self.SAF,\
		self.State =\
		(0,-1,0.0,\
			-1.0,0.0,[-3,-2,-1],\
			False,False,False,\
			SS)	

	def is_flow_done(self):				
		if self.LPIA == len(self.tx_buffer)-1:
			return 1
		return 0

	def send(self,p):			
		p.set_in_transit(1)
		p.set_tx_time(self.sim.get_current_time())
		self.EPIT += 1					

		self.sim.request_event(\
			Time_Out_Packet(p, \
							self.sim.get_current_time() + constants.DATA_PACKET_TIMEOUT))
		self.sim.get_element(self.source).send(p)		
		self.debug_log_reno_source(False,"send",p.get_ID())

	def replaceDataPacket (self,pid):
		q = Packet(self, self.source, self.dest, \
				constants.DATA_PACKET_TYPE, pid, \
				constants.DATA_PACKET_BITWIDTH)
		self.tx_buffer[q.get_ID()] = q

	def updateRTTactEst(self, ack):
		self.RTTactBuff.pop(0)		
		self.RTTactBuff.append(self.sim.get_current_time() - ack.get_tx_time())

		RTTact = self.linearRTTAverage()		

		if RTTact > 0:
			self.RTTactEst = RTTact
		else:
			raise ValueError("Somehow received a 0 or negative RTT at time %0.6e with tx_time %0.6e, at packet %d"%(self.sim.get_current_time(), ack.get_tx_time(), ack.get_ID()))

	def linearRTTAverage(self):
		RTTact = 0
		cnt = 0.0
		for m in xrange(len(self.RTTactBuff)):
			if self.RTTactBuff[m] >= 0:
				RTTact += self.RTTactBuff[m]
				cnt += 1.0
		RTTact /= cnt
		return RTTact

	# We set the STT on timeouts to avoid responding to packets that we 
	# thought were timed out.
	def time_out(self,packet):
		if not packet.get_timeout_disabled():						
			self.EPIT = max(self.EPIT-1,0)
			# Replace the packet that timed out with a fresh one
			self.replaceDataPacket(packet.get_ID())

			if not (self.State == TR):
				self.State = TR
				self.STT = self.sim.get_current_time()
				self.CAT = max(self.WS/2,1.0)			# NOT CAT/2
				self.L3P = [-3, -2, -1]			
				self.WS = 1.0
			self.debug_log_reno_source(True,"timeout",packet.get_ID())				
			if self.EPIT < self.WS:
				self.State = SS
				self.transmit()					

	# called on the first recognition of a triple-ack		
	def setup_fr(self):			
		# disables timeout on the packet triple acked in L3P
		tripleAckdPacket = self.L3P[2] + 1 
		self.tx_buffer[tripleAckdPacket].set_timeout_disabled(True)
		self.replaceDataPacket(tripleAckdPacket)
		self.EPIT = max(self.EPIT-1,0)		

	# From WS & EPIT & Tx_Buffer, determines how many packets to send	
	def transmit(self):
		for m in xrange(len(self.tx_buffer)):
			if self.EPIT < int(math.floor(self.WS)):
				if (self.tx_buffer[m].get_in_transit() == 0) and (self.tx_buffer[m].get_ack() == 0):
					self.send(self.tx_buffer[m])
			else:
				break			
	
	# initialization from event simulator
	def start(self):		
		self.WS = 1.0
		self.EPIT = 0
		self.STT = self.sim.get_current_time()
		self.L3P = [-3, -2, -1]				
		self.LPIA = -1
		self.CAT = -1.0
		self.State = SS
		RTTactBuff = [-1] * constants.FAST_RTT_WINDOW_SIZE
		RTTactEst = -1	
		self.updateCount = FAST_UPDATE_PERCENTAGE_DELAY
		self.debug_log_reno_source(False,"start",self.LPIA)
		self.transmit()		

	# log all state. isTimeoutOccurring is a boolean (True/False), SendReceive ("send","receive","start","timeout"), whichPacket (ID)
	def debug_log_reno_source(self,isTimeoutOccurring,SendReceive,whichPacket):	
		if MEASUREMENT_ENABLE:
			print MEASURE_FLOW_RENO_FULL_DEBUG((self,\
											SendReceive,\
											whichPacket,\
											self.EPIT,\
											self.LPIA,\
											self.WS,\
											self.CAT,\
											self.STT,\
											self.L3P[0],\
											self.L3P[1],\
											self.L3P[2],\
											self.TAF,self.DAF,self.SAF,\
											self.State,\
											isTimeoutOccurring,\
											self.RTTactEst,\
											self.sim.get_current_time()))		

	''' 
	It is possible for a string of timeouts to occur even though the actual packets
	are still in the network. Then, we start sending new packets, and later receive
	acks for the old packets. This means it is possible for a Timeout Ack to set the LPIA,
	and for a packet with tx
	_time >= STT to ack something that doesn't set the LPIA.

	This means NAC would be 0, and without corrective action we would not set EPIT properly.
	However, remember that it is also possible for normal packets to arrive out of order,
	so it is entirely possible to receive a packet >= STT that is not supposed to set LPIA,
	because it was overtaken, and therefore EPIT has already been accounted for. 

	To deal with this, if a timeout ack (tx_time < STT) set the last LPIA, and we see a new >=STT packet, and it 
	doesn't set the LPIA, then we reset EPIT based on a count of in-transit accounted packets.
	
	If a tx_time >= STT packet does not set the LPIA, NAC = 0. In this case, we forbit the ack from changing WS. 
	We're being conservative. 

	This isn't guaranteed to work. Say we have timeouts and start sending packets again, then receive those 'timed out acks'
	in disparate bursts, because of some weird dynamic routing. We might send packets 2-3 times unnecessarily as we realize
	in spurts what the sink has really seen. So we'll keep reducing EPIT based on timeout (when we see new >= STT acks)
	so we'll send out 4 packets, receive a timeout ack, receive an ack from ONE of those packets we just sent, and immediately
	set EPIT - 4 (since the timeout was from way further ahead) and send out 4 new packets. 

	Then as we receive the other 3 packets from our original 4, we won't change WS or EPIT at all, but now we could actually have
	7 packets in the network. So our EPIT (4) is almost 100 percent off. 

	You could also imagine this going the other way, with a packet Ack beating timed out acks due to weird routing,
	taking credit for clearing the network when actually most of our packets are still out there. 

	I suppose the hope is congestion control keeps us close enough to a reasonable network throughput that this doesn't get_
	out of hand. It might also be a reason for static routing over dynamic routing, to avoid such packets-out-of-order
	issues. 

	TL;DR It's safest to do the following: 
		On TO acks, we update LPIA, but not EPIT or WS or State
		On normal acks, we update LPIA, and count EPIT anew. If there is an EPIT difference (either because this is a normal ack moving things along, 
			or because we're seeing TO acks leaving the network and were not allowed to update EPIT before) we may update WS, otherwise we cannot. 		
	'''
	def recountEPIT(self):		
		currEPIT = self.EPIT
		
		nextEPIT = 0		
		for m in xrange(len(self.tx_buffer)):
			if (self.tx_buffer[m].get_in_transit() == 1):
				nextEPIT += 1
		
		self.EPIT = nextEPIT

		deltaEPIT = abs(nextEPIT - currEPIT)
		return deltaEPIT
	
	def handleAck(self,pid):
		'''
		Set acks up to Ack packet ID if needed
			Set RTT for those packets 
			Reset in transit for those packets
			if State != TR:
				at the same time as you reset in transit, 
				Set ignore timeout flags in packets up to Ack packet ID			
		Update LPIA
		'''
		for m in xrange(len(self.tx_buffer)):
			if pid >= m:					
				self.tx_buffer[m].set_ack(1)
				self.tx_buffer[m].set_in_transit(0)
				if not (self.State == TR):
					self.tx_buffer[m].set_timeout_disabled(True)
			else:
				break
		if pid > self.LPIA:
			self.LPIA = pid
			if self.updateCount < 0:
				percentDone = int(100.0*(self.LPIA+1.0) / len(self.tx_buffer)) 
				sys.stderr.write("Flow %s is %d%s complete.\n"%(self.get_id().split("_")[0],percentDone,'%'))
				self.updateCount = FAST_UPDATE_PERCENTAGE_DELAY
			else:
				self.updateCount -= 1

	def updateL3P(self,pid):
		# Update 3-deep Ack Memory 
		self.L3P.pop(0)
		self.L3P.append(pid)

	def setFlags(self):
		# Set TAF,DAF,SAF flags					
		# Do not worry about misordered packets (for now)
		self.TAF = True if (self.L3P[0] == self.L3P[1]) and (self.L3P[1] == self.L3P[2]) else False
		self.DAF = True if (self.L3P[1] == self.L3P[2]) and (not self.TAF) else False
		self.SAF = not (self.TAF or self.DAF)

	def chooseNextState(self):
		# Choose current state based on previous state, WS, and 3-Ack memory
		if self.State == TR:
			self.State = TR
		elif self.State == SS:				
			if self.SAF:
				if self.CAT < 0 or self.WS < int(math.floor(self.CAT)):
					self.State = SS
				else:						
					self.State = CA
			elif self.DAF:
				self.State = SS
			elif self.TAF:	
				self.WS = max(self.WS/2,1.0)
				self.CAT = self.WS
				self.setup_fr()
				self.State = FR								
		elif self.State == CA:
			if self.SAF:
				self.State = CA
			elif self.DAF:
				self.State = CA
			elif self.TAF:
				self.WS = max(self.WS/2,1.0)
				self.setup_fr()
				self.State = FR			
		elif self.State == FR:
			if self.SAF:
				self.WS = max(self.WS/2,1.0)
				self.State = CA
			elif self.TAF:
				self.State = FR
			else:
				raise ValueError("Should never have gotten to self.DAF in FR")
		else:
			raise ValueError("What state is RENO in?")					

	def operateFromState(self,deltaEPIT):
		# Operate from current state
		if self.State == TR:
			# do nothing, wait for all to time out, even if received some
			# insofar as is possible want to clear our congestion				
			pass
		else:
			if (not (self.State == FR)) and (deltaEPIT > 0):
				if self.State == SS:	
					self.WS += 1
				elif self.State == CA:
					self.WS += 1.0/self.WS					
			elif self.State == FR:						
				self.WS += 1								
			self.transmit()	

	def receive(self,packet):
		pid = packet.get_ID()			
		self.handleAck(pid)
		self.updateRTTactEst(packet)		
		self.debug_log_reno_source(False,"receive",pid)			

		'''
		When we check Ack packets, we'll use them to make next-Packet decisions,
		but only use them to update state (i.e. as a measure of congestion)
		if their timestamp is greater than our STT.				
		Checking >= STT forces us, in TR, to wait for the timeout of every packet in our window
		somewhat clearing our congestion from the network, before starting again
		also ensures we don't respond to acks from previous timeout cycles in our current CC
		'''
		if packet.get_tx_time() >= self.STT:			
			deltaEPIT = self.recountEPIT()						
			self.updateL3P(pid)
			self.setFlags()			
			self.chooseNextState()
			self.operateFromState(deltaEPIT)