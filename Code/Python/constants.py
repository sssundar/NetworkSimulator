# Constants File 

# Packet Types 
DATA_PACKET_ACKNOWLEDGEMENT_TYPE = "ACK_DATA"
DATA_PACKET_TYPE = "DATA"

# Packet Sizes
DATA_PACKET_BITWIDTH = 8 # in kbits (so 1 kbyte packet)
DATA_ACK_BITWIDTH = 0.064 # 8 bytes, 0.064 kbits

# Data Flow Packet Timeout
DATA_PACKET_TIMEOUT = 100.0 # ms

# Link Transmission Directions
RTL = "right-to-left"
LTR = "left-to-right"

# Test Case Filenames
TESTCASE0 = "input_test0.json"
TESTCASE1 = "input_test1.json"

#############################################
# Logging Measurement Functions & Constants #
#############################################

# Measurement Enable, to make logging-unrelated debugging faster
MEASUREMENT_ENABLE = True

LINKRATE_MEASUREMENT_BASE = \
"\n{\"logtype\":\"measurement\",\"measurement\":\"linkrate\",\"linkid\":\"%s\",\
\"mbits_propagated\":\"%0.3e\",\"ms_globaltime\":\"%0.6e\"}\n"

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
\"fractional_buffer_occupancy\":\"%0.3e\",\"ms_globaltime\":\"%0.6e\"}\n"

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

