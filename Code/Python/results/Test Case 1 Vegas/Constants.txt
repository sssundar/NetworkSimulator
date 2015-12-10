# Constants File # 

###################
# USER MODIFIABLE #
###################

# Plotting ms-binning Window
MS_WINDOW = 100 # ms, for binning	

# TCP and Routing Thresholds

# VEGAS
FAST_CA_THRESHOLD = 5.0 # when RTTact ~ 3x RTTmin, transition from SS to CA
SS2CA_SCALING = 0.875
VEGAS_ALPHA = 0.4
VEGAS_BETA = 0.45

# FAST
FAST_ALPHA = 20.0 	
FAST_RTT_WINDOW_SIZE = int(15) # estimate RTTact from FAST_RTT_WINDOW_SIZE last RTTs
FAST_WS_UPDATE_TIME = 220.0 # ms ~timescale of a few packet arrivals to re-estimate RTT
FAST_TO_RTTMAX_SCALAR = 3.0 # times RTTmax as the timeout penalty
FAST_TO_ALLOWANCE = 3.0 # times RTTactEst as the timeout allowance
FAST_BASE_RTTMAX = 1000.0 # ms (in case of timeout on first send)
FAST_EXPONENTIAL_DECAY = float(0.1) # 10 samples back, will see 1/e weighting

FAST_UPDATE_PERCENTAGE_DELAY = 100 # packets per % complete update

# Link Queueing Memory
QUEUEING_DELAY_WINDOW = 20

# Interval to wait before sending new ROUTER packets to update the table
ROUTING_TABLE_UPDATE_PERIOD = 6000.0 # ms

# Data Flow Packet Timeout
DATA_PACKET_TIMEOUT = 4000.0 # ms_globaltime


#################################
# MODIFY BELOW AT YOUR OWN RISK #
#################################

# TCP RENO/FAST States
SS = 1
CA = 2
FR = 3
TR = 4

# Packet Types 
DATA_PACKET_ACKNOWLEDGEMENT_TYPE = "ACK_DATA"
DATA_PACKET_TYPE = "DATA"
ROUTER_PACKET_ACKNOWLEDGEMENT_TYPE = "ACK_ROUTER"  
ROUTER_PACKET_TYPE = "ROUTER"

ROUTER_FLOW = "0"

# Packet Sizes
DATA_PACKET_BITWIDTH = 8 # in kbits (so 1 kbyte packet)
DATA_ACK_BITWIDTH = 0.512 # 64 bytes, 0.512 kbits
DATA_ROUTER_BITWIDTH = 0.064 # 8 bytes, Requesting table
DATA_ROUTER_ACK_BITWIDTH = 1 # kbits 

# Link Transmission Directions
RTL = "right-to-left"
LTR = "left-to-right"

# Test Case Filenames
TESTCASE0 = "input_test0.json"
TESTCASE1 = "input_test1.json"

# Select TCP
TCP_RENO = 'reno'
TCP_FAST = 'fast'
TCP_VEGAS = 'vegas'

#############################################
# Logging Measurement Functions & Constants #
#############################################

# Measurement Enable, to make logging-unrelated debugging faster
MEASUREMENT_ENABLE = True

LINKRATE_MEASUREMENT_BASE = \
"\n{\"logtype\":\"measurement\",\"measurement\":\"linkrate\",\"linkid\":\"%s\",\
\"mbits_propagated\":\"%0.6e\",\"ms_globaltime\":\"%0.6e\"}\n"

# takes link object reference, takes kbits propagated to end of link at t=time
# prints measurements directly to stdout:
# mbits propagated, time (ms) in format 0.3e
MEASURE_LINKRATE = lambda ((link,kbits_propagated,time)):\
	LINKRATE_MEASUREMENT_BASE % ((	link.get_id(),\
									float(kbits_propagated)/1000,\
									time)\
		)


BUFFER_OCCUPANCY_MEASUREMENT_BASE = \
"\n{\"logtype\":\"measurement\",\"measurement\":\"bufferoccupancy\",\
\"linkid\":\"%s\",\"direction\":\"%s\",\
\"fractional_buffer_occupancy\":\"%0.6e\",\"ms_globaltime\":\"%0.6e\"}\n"

# Units: Percent full, since packets have variable bit width
# Windowing on logs of changes will not give us the correct result.
# We need to account for the timing, i.e. the % of time we were at each level,
# within our binning window. A true time average. So we can add deltas,
# and remember the starting value looking into each window on each side.
# Ok: Have each link log the buffer size for each side, every time it changes.
# Include a timestamp.
MEASURE_BUFFER_OCCUPANCY = \
	lambda ((link,direction_of_buffer,fractional_occupancy,ms_time)):\
		BUFFER_OCCUPANCY_MEASUREMENT_BASE % ((	link.get_id(),\
											direction_of_buffer,\
											fractional_occupancy,\
											ms_time)\
			)

PACKET_LOSS_MEASUREMENT_BASE = \
"\n{\"logtype\":\"measurement\",\"measurement\":\"packetloss\",\
\"flowid\":\"%s\",\"packettype\":\"%s\",\"packetid\":\"%s\",\"ms_globaltime\":\"%0.6e\"}\n"

# Units: packets
# Have each link log each packet it drops with the flow, and time
# Flows being separated into sources and sinks, we can tell which were
# acks and which were data. 
MEASURE_PACKET_LOSS = \
	lambda ((flow,packet_type,packet_id,ms_time)):\
		PACKET_LOSS_MEASUREMENT_BASE % (flow.get_id(), packet_type, packet_id, ms_time)

FLOWRATE_MEASUREMENT_BASE = \
"\n{\"logtype\":\"measurement\",\"measurement\":\"flowrate\",\"flowid\":\"%s\",\
\"mbits_received_at_sink\":\"%0.6e\",\"ms_globaltime\":\"%0.6e\"}\n"

MEASURE_FLOWRATE = lambda ((flow,kbits_propagated,time)):\
	FLOWRATE_MEASUREMENT_BASE % ((	flow.get_id(),\
									float(kbits_propagated)/1000,\
									time)\
		)

# flow window size in packets
FLOW_WINDOW_SIZE_MEASUREMENT_BASE = \
"\n{\"logtype\":\"measurement\",\"measurement\":\"windowsize\",\
\"flowid\":\"%s\",\
\"windowsize\":\"%0.6e\",\"ms_globaltime\":\"%0.6e\"}\n"

MEASURE_FLOW_WINDOW_SIZE = \
	lambda ((flow,windowsize,ms_time)):\
		FLOW_WINDOW_SIZE_MEASUREMENT_BASE % ((	flow.get_id(),\
											windowsize,\
											ms_time)\
			)


# packet rtt in milliseconds
PACKET_RTT_MEASUREMENT_BASE = \
"\n{\"logtype\":\"measurement\",\"measurement\":\"packetrtt\",\
\"flowid\":\"%s\",\
\"packetrtt\":\"%0.6e\",\"ms_globaltime\":\"%0.6e\"}\n"

MEASURE_PACKET_RTT = \
	lambda ((flow,ms_packetrtt,ms_time)):\
		PACKET_RTT_MEASUREMENT_BASE % ((	flow.get_id(),\
											ms_packetrtt,\
											ms_time)\
			)

# TCP State Measurement {SlowStart=1,Fr/FT=2,CA=3}
FLOWSTATE_MEASUREMENT_BASE = \
"\n{\"logtype\":\"measurement\",\"measurement\":\"flowstate\",\
\"flowid\":\"%s\",\
\"state\":\"%d\",\"ms_globaltime\":\"%0.6e\"}\n"

SlowStartID = 1
FrFtID = 2
CongestionAvoidanceID = 3

MEASURE_FLOW_STATE = \
	lambda ((flow,state,ms_time)):\
		FLOWSTATE_MEASUREMENT_BASE % ((	flow.get_id(),\
											state,\
											ms_time)\
			)

FLOW_OUTSTANDINGPACKETS_MEASUREMENT_BASE = \
"\n{\"logtype\":\"measurement\",\"measurement\":\"outstandingpackets\",\
\"flowid\":\"%s\",\
\"packets_out\":\"%d\",\
\"packets_left\":\"%d\",\
\"packets_in_transit\":\"%d\",\
\"packets_ackd\":\"%d\",\
\"total_packets\":\"%d\",\
\"ms_globaltime\":\"%0.6e\"}\n"

MEASURE_FLOW_OUTSTANDING = \
	lambda ((flow,\
		packets_out,\
		packets_left,\
		packets_in_transit,\
		packets_ackd,\
		total_packets,\
		ms_time)):\
		FLOW_OUTSTANDINGPACKETS_MEASUREMENT_BASE % ((	flow.get_id(),\
											packets_out,\
											packets_left,\
											packets_in_transit,\
											packets_ackd,\
											total_packets,\
											ms_time)\
			)

FLOW_RENO_FULL_DEBUG_MEASUREMENT_BASE = \
"\n{\"logtype\":\"measurement\",\"measurement\":\"fullrenodebug\",\
\"flowid\":\"%s\",\
\"SendReceive\":\"%s\",\
\"whichPacket\":\"%d\",\
\"EPIT\":\"%d\",\
\"LPIA\":\"%d\",\
\"WS\":\"%0.3e\",\
\"CAT\":\"%0.3e\",\
\"STT\":\"%0.6e\",\
\"L3P0\":\"%d\",\
\"L3P1\":\"%d\",\
\"L3P2\":\"%d\",\
\"TAF\":\"%s\",\
\"DAF\":\"%s\",\
\"SAF\":\"%s\",\
\"State\":\"%d\",\
\"isTimeoutOccurring\":\"%s\",\
\"RTTactEst\":\"%0.6e\",\
\"ms_globaltime\":\"%0.6e\"}\n"

MEASURE_FLOW_RENO_FULL_DEBUG = \
	lambda ((flow,\
		SendReceive,\
		whichPacket,\
		EPIT,\
		LPIA,\
		WS,\
		CAT,\
		STT,\
		L3P0,\
		L3P1,\
		L3P2,\
		TAF,DAF,SAF,\
		State,\
		isTimeoutOccurring,\
		RTTactEst,\
		ms_time)):\
		FLOW_RENO_FULL_DEBUG_MEASUREMENT_BASE % ((	flow.get_id(),\
											SendReceive,\
											whichPacket,\
											EPIT,\
											LPIA,\
											WS, CAT, STT,\
											L3P0, L3P1, L3P2,\
											TAF,DAF,SAF,\
											State,\
											isTimeoutOccurring,\
											RTTactEst,\
											ms_time)\
			)

FLOW_VEGAS_FULL_DEBUG_MEASUREMENT_BASE = \
"\n{\"logtype\":\"measurement\",\"measurement\":\"fullvegasdebug\",\
\"flowid\":\"%s\",\
\"SendReceive\":\"%s\",\
\"whichPacket\":\"%d\",\
\"EPIT\":\"%d\",\
\"LPIA\":\"%d\",\
\"WS\":\"%0.3e\",\
\"STT\":\"%0.6e\",\
\"L3P0\":\"%d\",\
\"L3P1\":\"%d\",\
\"L3P2\":\"%d\",\
\"TAF\":\"%s\",\
\"DAF\":\"%s\",\
\"SAF\":\"%s\",\
\"State\":\"%d\",\
\"FlagObserveRTT\":\"%s\",\
\"FlagRampWS\":\"%s\",\
\"isTimeoutOccurring\":\"%s\",\
\"RTTmin\":\"%0.6e\",\
\"RTTactEst\":\"%0.6e\",\
\"ICAPTUW\":\"%d\",\
\"ms_globaltime\":\"%0.6e\"}\n"

MEASURE_FLOW_VEGAS_FULL_DEBUG = \
	lambda ((flow,
		SendReceive,\
		whichPacket,\
		EPIT,\
		LPIA,\
		WS,\
		STT,\
		L3P0,\
		L3P1,\
		L3P2,\
		TAF,DAF,SAF,\
		State,\
		isTimeoutOccurring,\
		RTTmin,RTTactEst,Packets_Till_Update_WS_IN_CA,\
		FlagObserveRTT,FlagRampWS,\
		ms_time)):\
		FLOW_VEGAS_FULL_DEBUG_MEASUREMENT_BASE % ((	flow.get_id(),\
											SendReceive,\
											whichPacket,\
											EPIT,\
											LPIA,\
											WS, STT,\
											L3P0, L3P1, L3P2,\
											TAF,DAF,SAF,\
											State,\
											FlagObserveRTT, FlagRampWS,\
											isTimeoutOccurring,\
											RTTmin,RTTactEst,\
											Packets_Till_Update_WS_IN_CA,\
											ms_time)\
			)

FLOW_FAST_FULL_DEBUG_MEASUREMENT_BASE = \
"\n{\"logtype\":\"measurement\",\"measurement\":\"fulltruefastdebug\",\
\"flowid\":\"%s\",\
\"SendReceive\":\"%s\",\
\"whichPacket\":\"%d\",\
\"EPIT\":\"%d\",\
\"LPIA\":\"%d\",\
\"WS\":\"%0.3e\",\
\"STT\":\"%0.6e\",\
\"L3P0\":\"%d\",\
\"L3P1\":\"%d\",\
\"L3P2\":\"%d\",\
\"TAF\":\"%s\",\
\"DAF\":\"%s\",\
\"SAF\":\"%s\",\
\"isTimeoutOccurring\":\"%s\",\
\"RTTmin\":\"%0.6e\",\
\"RTTmax\":\"%0.6e\",\
\"RTTactEst\":\"%0.6e\",\
\"ms_globaltime\":\"%0.6e\"}\n"

MEASURE_FLOW_FAST_FULL_DEBUG = \
	lambda ((flow,
		SendReceive,\
		whichPacket,\
		EPIT,\
		LPIA,\
		WS,\
		STT,\
		L3P0,\
		L3P1,\
		L3P2,\
		TAF,DAF,SAF,\
		isTimeoutOccurring,\
		RTTmin,RTTmax,RTTactEst,\
		ms_time)):\
		FLOW_FAST_FULL_DEBUG_MEASUREMENT_BASE % ((	flow.get_id(),\
											SendReceive,\
											whichPacket,\
											EPIT,\
											LPIA,\
											WS, STT,\
											L3P0, L3P1, L3P2,\
											TAF,DAF,SAF,\
											isTimeoutOccurring,\
											RTTmin,RTTmax,RTTactEst,\
											ms_time)\
			)
