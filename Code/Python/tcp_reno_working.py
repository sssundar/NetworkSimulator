# TCP Reno Flow - Specification
# Last Revised 
#	by Sushant Sundaresh on 24 November 2015
# 		Gutted, Restructured

''' 
This flow keeps track of:
	EPIT: estimated packets in transit
	PSUA: packets sent but unacknowledged
	PSAA: packets sent and acknowledged
	PUUA: packets unsent and unacknowledged

	WS: window size
	CAT: congestion avoidance threshold from slow start
	STT: send-time threshold 

	States
		SS, slow start (WS+=1)
		CA, congestion avoidance (WS+=1/WS)
		FR, fast retransmit, fast recover (WS+=1)		
		TR, timeout recovery

Operation	
	Packets will be sent out with a timestamp local to the machine.
	This will be preserved in the Ack packet.

	When we check Ack packets, we'll use them to make next-Packet decisions,
	but only use them to update state (i.e. as a measure of congestion)
	if their timestamp is greater than our STT.

	We set the STT on timeouts to avoid responding to packets that we 
	thought were timed out.

	During TR we can respond to STT violating packet Acks to bring EPIT down. 
	We won't update state from TR, but will set EPIT -= 1.

	On receiving a packet:
		Update transmission memory if necessary 
			Set acks up to Ack packet ID
			Reset in transit up to Ack packet ID
			Set ignore timeout flags up to Ack packet ID
		If State = TR | timestamp >= STT:					
			Update EIPT
		If timestamp >= STT:
			Update 3-deep Ack Memory
		Choose state based on previous state and 3-Ack memory
		Operate from state
			From SS:	
				(WS = CAT) => enter CR
				Single Ack => WS+= 1
				Double Ack => pass
				Triple Ack => enter FR with WS /= 2 and CAT = WS/2 		
				Timeout => enter TR with CAT = WS/2 then set WS = 1, setting new STT
			From CR:
			From FR:	
				FR/FT should check that an Ack had some effect before releasing control. 

Functions	
	void start ():
		Enters slow start as though for the first time
	void enter_ss ():
	void enter_ca ():
	void enter_fr ():
	void enter_to ():
	void set_cat ():
		Sets CAT to half the current window size	
	void receive ():
		receives a packet, updates state, transmits new packet if it can
	bool can_transmit ():
		figure out whether a packet may be transmitted
	void transmit ():
		figures out next packet to transmit, and transmits it
	void log_state ():
		logs all recorded state to STDOUT 

'''

