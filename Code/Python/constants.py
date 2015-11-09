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

# Logging Message Identifiers
LOGHEADER = "DEBUG LOG: "