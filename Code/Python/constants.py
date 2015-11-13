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
'''
LINKRATE_MEASUREMENT_BASE = \
"\n{\"logtype\":\"measurement\", \"measurement\":\"linkrate\", \"linkid\":\"%s\", \
\"bits\":\"%d\",\"globaltime\":\"%0.3fms\"}\n"

## kbits / 1000 should be float.
@$%#$
MEASURE_LINKRATE = lambda ((link,kbits_propagated,time)):\
	print LINKRATE_MEASUREMENT_BASE % ((	link.get_id(),\
									int(float(kbits_propagated)/1000),\
									time)\
	)

# takes link object reference
# take kbits propagated at time
# prints directly to stdout
# Mbps, time (ms) with 3 fractional decimal precision digits.
'''