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

# Logging Measurement Functions & Constants

LINKRATE_MEASUREMENT_BASE = \
"\n{\"logtype\":\"measurement\",\"measurement\":\"linkrate\",\"linkid\":\"%s\",\
\"mbits_propagated\":\"%0.3e\",\"ms_globaltime\":\"%0.3e\"}\n"

# takes link object reference, takes kbits propagated to end of link at t=time
# prints measurements directly to stdout:
# mbits propagated, time (ms) in format 0.3e
MEASURE_LINKRATE = lambda ((link,kbits_propagated,time)):\
	LINKRATE_MEASUREMENT_BASE % ((	link.get_id(),\
									float(kbits_propagated)/1000,\
									time)\
		)

# Test Case Filenames
TESTCASE0 = "input_test0.json"
TESTCASE1 = "input_test1.json"