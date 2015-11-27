# Constants File 

# Packet Types 
DATA_PACKET_ACKNOWLEDGEMENT_TYPE = "ACK_DATA"
DATA_PACKET_TYPE = "DATA"
ROUTER_PACKET_ACKNOWLEDGEMENT_TYPE = "ACK_ROUTER"
ROUTER_PACKET_TYPE = "ROUTER"

# Packet Sizes
DATA_PACKET_BITWIDTH = 8 # in kbits (so 1 kbyte packet)
DATA_ACK_BITWIDTH = 0.064 # 8 bytes, 0.064 kbits

# Data Flow Packet Timeout
DATA_PACKET_TIMEOUT = 500.0 # ms_globaltime

# Link Transmission Directions
RTL = "right-to-left"
LTR = "left-to-right"

# Test Case Filenames
TESTCASE0 = "input_test0.json"
TESTCASE1 = "input_test1.json"

# Select TCP
TCP_RENO_ENABLE = True
TCP_FAST_ENABLE = False
TCP_STATIC_ENABLE = False

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
