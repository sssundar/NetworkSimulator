'''
# TCP Fast Flow Source - Specification
# TCP Fast Flow Sink is the same as Reno
# Last Revised 
#	by Sushant Sundaresh on 5 December 2015

References: TAs (Ritvik)
	Turns out TCP FAST is not drop based at all.
	That is, it's not just an extension of Vegas.
	There are no SS/FR/FT/TR states.
	There is only CA with window updates on a fixed period. 	
	
	We need a timeout with a fixed period on which we update WS as 
		WS =  RTTmin/RTTact * WS + alpha 

	We need to track RTTmin, RTTact (averaged over last 20 packets, say), maxRTT.

	On timeouts, we set the packet RTT to some constant factor (2, say) times our max RTT observed,
	update our WS pre-emptively, and proceed as normal.	

	On triple acks we preemptively count a packet as 'dropped,' and proceed as normal.
'''

from reporter import Reporter
from packet import *
import math
from constants import *
from events import *
from flow import *
import sys

class Working_Data_Source_TCP_FAST(Data_Source):
	EPIT = 0 # estimated packets in transit

	LPIA = -1 # last packet id acknowledged

	WS = 0.0 # window size
		
	L3P = [-3, -2, -1] # last three packet ids

	TAF = False #	TAF triple ack 
	DAF = False #	DAF double ack
	SAF = False #	SAF single ack 	

	RTTmin = -1
	RTTmax = -1
	RTTactBuff = [-1] * constants.FAST_RTT_WINDOW_SIZE
	RTTactEst = -1	

	def __init__(self, identity, src, sink, size, start):
		Data_Source.__init__(self, identity, src, sink, size, start)	
		
		self.EPIT, self.LPIA, self.WS,\
		self.L3P,\
		self.TAF, self.DAF, self.SAF,\
		self.RTTmin, self.RTTmax, self.RTTactBuff,RttactEst=\
		(0,-1,0.0,\
			[-3,-2,-1],\
			False,False,False,\
			-1, -1, [-1]*constants.FAST_RTT_WINDOW_SIZE,-1)

	def is_flow_done(self):				
		if self.LPIA == len(self.tx_buffer)-1:
			return 1
		return 0

	# initialization from event simulator
	def start(self):		
		self.WS = 1.0
		self.EPIT = 0		
		self.L3P = [-3, -2, -1]				
		self.LPIA = -1							
		self.RTTmin = -1
		self.RTTmax = -1
		self.RTTactBuff = [-1] * constants.FAST_RTT_WINDOW_SIZE
		self.RTTactEst = -1		
		self.debug_log_fast_source(False,"start",self.LPIA)
		self.sim.request_event(FAST_WS_Update_Callback(self,self.sim.get_current_time()+constants.FAST_BASE_RTTMAX))
		self.transmit()		

	def updateRTTmin(self,ack):
		if (self.sim.get_current_time() - ack.get_tx_time() < self.RTTmin) or (self.RTTmin < 0):
			self.RTTmin = self.sim.get_current_time() - ack.get_tx_time()
		if self.RTTmin < 0:
			raise ValueError("Somehow received a negative RTT at time %0.6e with tx_time %0.6e, at packet %d"%(self.sim.get_current_time(), ack.get_tx_time(), ack.get_ID()))

	def updateRTTmax(self,ack):
		if (self.RTTmax < 0) or (self.sim.get_current_time() - ack.get_tx_time() > self.RTTmax):
			self.RTTmax = self.sim.get_current_time() - ack.get_tx_time()		
		if self.RTTmax < 0:
			raise ValueError("Somehow set RTTmax to a negative RTT at time %0.6e with tx_time %0.6e, at packet %d"%(self.sim.get_current_time(), ack.get_tx_time(), ack.get_ID()))

	# on timeout (toFlag), we assume a worst case tx_time
	def updateRTTactEst(self, toFlag, ack):
		if not toFlag:
			RTT = self.sim.get_current_time() - ack.get_tx_time()			
		elif self.RTTmax >= 0:
			RTT = self.RTTmax * FAST_TO_RTTMAX_SCALAR
		else:
			RTT = FAST_BASE_RTTMAX
		
		self.RTTactBuff.pop(0)		
		self.RTTactBuff.append(RTT)

		RTTact = self.linearRTTAverage()
		#RTTact = self.exponentialRTTAverage()

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

	# lower indices are further away in time
	def exponentialRTTAverage(self):
		RTTact = 0
		cnt = 0.0
		numSamples = len(self.RTTactBuff)
		for m in xrange(len(self.RTTactBuff)):
			if self.RTTactBuff[m] >= 0:
				RTTact += self.RTTactBuff[m] * math.exp(-1.0*float(numSamples-m-1)/FAST_EXPONENTIAL_DECAY)
				cnt += math.exp(-1.0*float(numSamples-m-1)/FAST_EXPONENTIAL_DECAY)
		RTTact /= cnt
		return RTTact

	# Timeout using scalar off RTTmax
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
							self.sim.get_current_time() + timeoutAllowance ))
		
		self.sim.get_element(self.source).send(p)		
		self.debug_log_fast_source(False,"send",p.get_ID())

	def replaceDataPacket (self,pid):
		q = Packet(self, self.source, self.dest, \
				constants.DATA_PACKET_TYPE, pid, \
				constants.DATA_PACKET_BITWIDTH)
		self.tx_buffer[q.get_ID()] = q

	# From WS & EPIT & Tx_Buffer, determines how many packets to send	
	def transmit(self):
		for m in xrange(len(self.tx_buffer)):
			if self.EPIT < int(math.floor(self.WS)):
				if (self.tx_buffer[m].get_in_transit() == 0) and (self.tx_buffer[m].get_ack() == 0):
					self.send(self.tx_buffer[m])
			else:
				break			
	
	# log all state. STT (-1) no longer exists.
	def debug_log_fast_source(self,isTimeoutOccurring,SendReceive,whichPacket):	
		if MEASUREMENT_ENABLE:
			print MEASURE_FLOW_FAST_FULL_DEBUG((self,\
											SendReceive,\
											whichPacket,\
											self.EPIT,\
											self.LPIA,\
											self.WS,\
											-1,\
											self.L3P[0],\
											self.L3P[1],\
											self.L3P[2],\
											self.TAF,self.DAF,self.SAF,\
											isTimeoutOccurring,\
											self.RTTmin,self.RTTmax,self.RTTactEst,\
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
				self.tx_buffer[m].set_timeout_disabled(True)
			else:
				break
		if self.LPIA < 0:
			sys.stderr.write("Percent Completion: 0")
		if pid > self.LPIA:
			self.LPIA = pid
			percentDone = int(100.0*(self.LPIA+1.0) / len(self.tx_buffer)) 									
			if percentDone == 100:
				sys.stderr.write("..100\n")
			elif (percentDone == 25) and (not self.flag25):			
				sys.stderr.write("..%d"%percentDone)
				self.flag25 = True
			elif (percentDone == 50) and (not self.flag50):			
				sys.stderr.write("..%d"%percentDone)
				self.flag50 = True				
			elif (percentDone == 75) and (not self.flag75):			
				sys.stderr.write("..%d"%percentDone)
				self.flag75 = True				

	def updateL3P(self,pid):
		self.L3P.pop(0)
		self.L3P.append(pid)

	def setFlags(self):
		self.TAF = True if (self.L3P[0] == self.L3P[1]) and (self.L3P[1] == self.L3P[2]) else False
		self.DAF = True if (self.L3P[1] == self.L3P[2]) and (not self.TAF) else False
		self.SAF = not (self.TAF or self.DAF)

	# On timeouts, we set the packet RTT to some constant factor (2, say) times our max RTT observed,
	# update our WS pre-emptively, and proceed as normal.
	def time_out(self,packet):
		if not packet.get_timeout_disabled():						
			self.EPIT = max(self.EPIT-1,0)
			# Replace the packet that timed out with a fresh one
			self.replaceDataPacket(packet.get_ID())
			# update window size with worst case RTT time
			self.to_update_ws()
			
			self.debug_log_fast_source(True,"timeout",packet.get_ID())				
			
			self.transmit()				

	def to_update_ws (self):
		self.updateRTTactEst(True,None)	
		self.benign_update_ws()

	def benign_update_ws (self):
		if self.RTTmin < 0:
			self.WS = 1.0
		else:
			self.WS = (self.RTTmin/self.RTTactEst)*self.WS + constants.FAST_ALPHA		

	# called on the first recognition of a triple-ack		
	# On triple acks we preemptively count a packet as 'dropped,' with a penalty
	# on our RTT buffer. We do not update our WS immediately; we proceed as normal.
	def setup_fr(self):			
		# disables timeout on the packet triple acked in L3P
		tripleAckdPacket = self.L3P[2] + 1 
		self.tx_buffer[tripleAckdPacket].set_timeout_disabled(True)
		self.replaceDataPacket(tripleAckdPacket)
		self.EPIT = max(self.EPIT-1,0)	
		self.updateRTTactEst(True,None)		
		self.debug_log_fast_source(False,"tripleack",tripleAckdPacket)				
	
	def receive(self,packet):
		if not (packet.get_type() == DATA_PACKET_ACKNOWLEDGEMENT_TYPE):
			raise ValueError("Flow %s, Packet Type %s, Source/Dest %s %s at time %0.6e\n"%(packet.get_flow().get_id(), packet.get_type(),packet.get_source(),packet.get_dest(),self.sim.get_current_time()))
		
		pid = packet.get_ID()			
		self.handleAck(pid)		
		self.updateRTTactEst(False,packet)		
		self.updateRTTmin(packet)
		self.updateRTTmax(packet)		
		
		deltaEPIT = self.recountEPIT()						
		self.updateL3P(pid)
		self.setFlags()			

		self.debug_log_fast_source(False,"receive",pid)			

		if self.TAF:
			self.setup_fr()

		self.transmit()	
			