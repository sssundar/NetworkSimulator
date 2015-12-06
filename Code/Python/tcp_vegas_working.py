'''
# TCP VEGAS Flow Source - Specification
# TCP VEGAS Flow Sink is the same as Reno
# Last Revised 
#	by Sushant Sundaresh on 5 December 2015

References: TCP Vegas, Modifications to Slow-Start, and FR/FT
			https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=3&cad=rja&uact=8&ved=0ahUKEwiTz8eltcDJAhVMxWMKHRVaAzEQFggxMAI&url=http%3A%2F%2Frenyang-learn.googlecode.com%2Fsvn%2Ftrunk%2Fns2%2FNS2_ppt%2FChapter%252010%2520TCP%2520Vegas.ppt&usg=AFQjCNHV2LP2hGgUaRQg0GdU8KadKyEeFQ&sig2=3eztvQii44rRlejfbYFEKA
References: TCP FAST Modifications to Vegas Congestion Avoidance
			http://courses.cms.caltech.edu/cs143/Slides/Low-201108-TCP-Cambridge.pdf
References: TAs (Ritvik)
	Turns out TCP FAST is not drop based at all. There are no SS/FR/FT/TR states.
	There is only CA with window updates on a fixed period. 
	I'm going to save this version, since it works, but rewrite for the correct FAST.
'''

'''
First Pass (Vegas with Updated CA)
FAST Algorithm Modifications, from RENO
	In all phases, we keep track of RTTmin (lowest ever observed) and RTTact (observed over an N-packet window, unweighted average)
	This in particular means we have to be very careful with Acks from TOs that were still in the network. 
	We should calculate RTT based on the current time & the Ack tx_time, if it's a timeout packet. 
	If there are multiple packets Ackd at once, we still only queue up one RTT based on the tx_time & current time (conservative)

	Start off in Slow-Start. Observe RTT and esimate RTTmin and RTTact.
		The congestion avoidance threshold is now a constant, and refers to the difference between RTTmin and RTTact.
		It can't be an absolute difference, it makes more sense for it to be a ratio.
		On hitting this threshold, set WS = 0.875 WS and proceed to CA.
		On TACK -> FR/FT
		On TO -> TR	

		We do not update WS each ack; we do so once every other WS (every 2 RTT). 
		It will suffice to keep track of whether we're in an observe or ramp slow-start phase.	

	In Congestion Avoidance
		Every time we clear our packet RTT history, we may update the WS according to:
		WS =  RTTmin/RTTact * WS + alpha 

		If we pretend this stabilizes to a constant RTTack, we can see we're really approaching
		a level of congestion where alpha sets how much queuing delay we're willing to accept. 

	In FR/FT
		Maybe I'm missing something, but Vegas' timeout condition for fast FR/FT would trigger a timeout and drop us into TR anyway
		So the only change here is to drop into CA based on the RTT act/min threshold as well.

	In TO recovery
		None	

We need to keep track of:

RTTmin
RTTact = [] with length constants.FAST_RTT_WINDOW_SIZE
Packets_Till_Update_WS_IN_CA = (in CA, start at FAST_RTT_WINDOW_SIZE, decrement, reset on 0) 

CAT = constants.FAST_CA_THRESHOLD
and constants.SS2CA_SCALING = 0.875

Within SS
	FlagObserveRTT
	FlagRampWS

'''

from reporter import Reporter
from packet import *
import math
from constants import *
from events import *
from flow import *
import sys

class Working_Data_Source_TCP_VEGAS(Data_Source):
	EPIT = 0 # estimated packets in transit

	LPIA = -1 # last packet id acknowledged

	WS = 0.0 # window size
	CAT = constants.FAST_CA_THRESHOLD # congestion avoidance threshold from slow start
	STT = 0.0 # send-time threshold 
	L3P = [-3, -2, -1] # last three packet ids

	TAF = False #	TAF triple ack 
	DAF = False #	DAF double ack
	SAF = False #	SAF single ack 

	State = SS

	RTTmin = -1	
	RTTactBuff = [-1] * constants.FAST_RTT_WINDOW_SIZE
	RTTactEst = -1
	Packets_Till_Update_WS_IN_CA = constants.FAST_RTT_WINDOW_SIZE

	FlagObserveRTT = False
	FlagRampWS = False

	mayUpdate = False

	updateCount = FAST_UPDATE_PERCENTAGE_DELAY 

	def __init__(self, identity, src, sink, size, start):
		Data_Source.__init__(self, identity, src, sink, size, start)					
		self.updateCount = FAST_UPDATE_PERCENTAGE_DELAY
		self.EPIT, self.LPIA, self.WS,\
		self.CAT, self.STT, self.L3P,\
		self.TAF, self.DAF, self.SAF,\
		self.State, self.RTTmin, self.RTTactBuff,RttactEst,\
		self.Packets_Till_Update_WS_IN_CA,\
		self.FlagObserveRTT, self.FlagRampWS, self.mayUpdateWS =\
		(0,-1,0.0,\
			constants.FAST_CA_THRESHOLD,0.0,[-3,-2,-1],\
			False,False,False,\
			SS, -1, [-1]*constants.FAST_RTT_WINDOW_SIZE,-1,\
			constants.FAST_RTT_WINDOW_SIZE,\
			False,False,False)

	def is_flow_done(self):				
		if self.LPIA == len(self.tx_buffer)-1:
			return 1
		return 0

	# initialization from event simulator
	def start(self):		
		self.WS = 1.0
		self.EPIT = 0
		self.STT = self.sim.get_current_time()
		self.L3P = [-3, -2, -1]				
		self.LPIA = -1		
		self.State = SS
		self.FlagObserveRTT = True
		self.updateCount = FAST_UPDATE_PERCENTAGE_DELAY
		self.FlagRampWS = False
		self.RTTmin = -1		
		self.RTTactBuff = [-1] * constants.FAST_RTT_WINDOW_SIZE
		self.RTTactEst = -1
		self.mayUpdateWS = False
		self.debug_log_vegas_source(False,"start",self.LPIA)
		self.transmit()		

	def updateRTTmin(self,ack):
		if (self.sim.get_current_time() - ack.get_tx_time() < self.RTTmin) or (self.RTTmin < 0):
			self.RTTmin = self.sim.get_current_time() - ack.get_tx_time()
		if self.RTTmin < 0:
			raise ValueError("Somehow received a negative RTT at time %0.6e with tx_time %0.6e, at packet %d"%(self.sim.get_current_time(), ack.get_tx_time(), ack.get_ID()))

	def updateRTTactEst(self, ack):
		RTT = self.sim.get_current_time() - ack.get_tx_time()
		self.RTTactBuff.pop(0)		
		self.RTTactBuff.append(RTT)
		RTTact = 0
		cnt = 0.0
		for m in xrange(len(self.RTTactBuff)):
			if self.RTTactBuff[m] >= 0:
				RTTact += self.RTTactBuff[m]
				cnt += 1.0
		RTTact /= cnt
		if RTTact > 0:
			self.RTTactEst = RTTact
		else:
			raise ValueError("Somehow received a negative RTT at time %0.6e with tx_time %0.6e, at packet %d"%(self.sim.get_current_time(), ack.get_tx_time(), ack.get_ID()))

	def send(self,p):			
		p.set_in_transit(1)
		p.set_tx_time(self.sim.get_current_time())
		self.EPIT += 1					

		timeoutAllowance = 0
		if self.RTTactEst >= 0:
			timeoutAllowance = self.RTTactEst * FAST_TO_ALLOWANCE
		else:
			timeoutAllowance = FAST_BASE_RTTMAX

		self.sim.request_event(\
			Time_Out_Packet(p, \
							self.sim.get_current_time() + timeoutAllowance))
		self.sim.get_element(self.source).send(p)		
		self.debug_log_vegas_source(False,"send",p.get_ID())

	def replaceDataPacket (self,pid):
		q = Packet(self, self.source, self.dest, \
				constants.DATA_PACKET_TYPE, pid, \
				constants.DATA_PACKET_BITWIDTH)
		self.tx_buffer[q.get_ID()] = q

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
				self.L3P = [-3, -2, -1]			
				self.WS = 1.0
			self.debug_log_vegas_source(True,"timeout",packet.get_ID())				
			if self.EPIT < self.WS:
				self.State = SS
				self.FlagObserveRTT = False
				self.FlagRampWS = True
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
	
	# log all state. packets till can update WS from CA is no longer relevant.
	def debug_log_vegas_source(self,isTimeoutOccurring,SendReceive,whichPacket):	
		if MEASUREMENT_ENABLE:
			print MEASURE_FLOW_VEGAS_FULL_DEBUG((self,\
											SendReceive,\
											whichPacket,\
											self.EPIT,\
											self.LPIA,\
											self.WS,\
											self.STT,\
											self.L3P[0],\
											self.L3P[1],\
											self.L3P[2],\
											self.TAF,self.DAF,self.SAF,\
											self.State,\
											isTimeoutOccurring,\
											self.RTTmin,self.RTTactEst,0,\
											self.FlagObserveRTT,self.FlagRampWS,\
											self.sim.get_current_time()))		

	def recountEPIT(self):		
		currEPIT = self.EPIT
		
		nextEPIT = 0		
		for m in xrange(len(self.tx_buffer)):
			if (self.tx_buffer[m].get_in_transit() == 1):
				nextEPIT += 1
		
		self.EPIT = nextEPIT

		deltaEPIT = abs(nextEPIT - currEPIT)
		return deltaEPIT
	
	flag25 = False
	flag50 = False
	flag75 = False
	def handleAck(self,pid):
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
				sys.stderr.write("Simulated transfer is %d%s complete.\n"%(percentDone,'%'))
				self.updateCount = FAST_UPDATE_PERCENTAGE_DELAY
			else:
				self.updateCount -= 1

	def updateL3P(self,pid):
		self.L3P.pop(0)
		self.L3P.append(pid)

	def setFlags(self):
		self.TAF = True if (self.L3P[0] == self.L3P[1]) and (self.L3P[1] == self.L3P[2]) else False
		self.DAF = True if (self.L3P[1] == self.L3P[2]) and (not self.TAF) else False
		self.SAF = not (self.TAF or self.DAF)

	def chooseNextState(self):
		if self.State == TR:
			self.State = TR
		elif self.State == SS:				
			if self.RTTactEst/self.RTTmin >= self.CAT:
				self.State = CA
				self.WS = max(self.WS * constants.SS2CA_SCALING, 1.0)
			else:			
				if self.SAF:
					if self.FlagObserveRTT:
						self.FlagObserveRTT = False
						self.FlagRampWS = True
					else:
						self.FlagObserveRTT = True
						self.FlagRampWS = False
					self.State = SS
				elif self.DAF:					
					self.State = SS	
				else:
					self.WS = max(self.WS/2,1.0)				
					self.setup_fr()
					self.State = FR								
		elif self.State == CA:
			if self.SAF or self.DAF:
				self.State = CA
			elif self.TAF:
				self.WS = max(self.WS/2,1.0)
				self.setup_fr()
				self.State = FR			
		elif self.State == FR:
			if (self.RTTactEst/self.RTTmin >= self.CAT) or self.SAF:
				self.State = CA
				self.WS = max(self.WS/2,1.0)
				self.WS = max(self.WS * constants.SS2CA_SCALING, 1.0)
			else:								
				if self.TAF:
					self.State = FR
				else:
					raise ValueError("Should never have gotten to self.DAF in FR")
		else:
			raise ValueError("What state is FAST in?")					

	def operateFromState(self,deltaEPIT):		
		if self.State == TR:
			pass
		else:
			if (self.State == SS) and (deltaEPIT > 0):				
				if self.FlagRampWS:
					self.WS += 1
			elif (self.State == CA):
				comp = (self.WS/self.RTTmin) - (self.WS/self.RTTactEst)
				#sys.stderr.write("%0.3e\n"%comp)
				if comp < VEGAS_ALPHA:
					self.WS += 1.0/self.WS
				elif comp > VEGAS_BETA:
					self.WS -= 1.0/self.WS
			elif self.State == FR:						
				self.WS += 1								
			self.transmit()	

	def receive(self,packet):
		pid = packet.get_ID()			
		self.handleAck(pid)		
		self.updateRTTactEst(packet)		
		self.updateRTTmin(packet)
		self.debug_log_vegas_source(False,"receive",pid)			

		if packet.get_tx_time() >= self.STT:			
			deltaEPIT = self.recountEPIT()						
			self.updateL3P(pid)
			self.setFlags()			
			self.chooseNextState()
			self.operateFromState(deltaEPIT)