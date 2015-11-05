# Packet Code
# Sith Domrongkitchaiporn

# The class Node extends the class Reporter
class Packet:

    flow = ""
    source = ""
    dest = ""
    typ = ""
    ID = -1
    bits = -1       # How big the packet is
    ack = 0         # Boolean (Has it been acknowledged)
    in_transit = 0  # Boolean
    tx_time = -1    
    ack_time = 1

    # Call Node initialization code, with the Node ID (required unique)
    # Initializes itself
    def __init__(self,flow,src,sink,typ,ID,bits):
        self.flow = flow              
        self.source = src
        self.dest = sink
        self.typ = typ
        self.ID = ID
        self.bits = bits

    def get_flow(self):
        return self.flow

    def get_source(self):
        return self.source

    def get_dest(self):
        return self.dest

    def get_ID(self):
        return self.ID

    def get_bits(self):
        return self.bits

    def get_ack(self): 
        return self.ack

    def get_in_transit(self):
        return self.in_transit

    def get_tx_time(self):
        return self.tx_time

    def get_ack_time(self):
        return self.ack_time

    def set_ack(self, flag):
        self.ack = flag

    def set_in_transit(self, flag):
        self.in_transit = flag

    def set_tx_time(self, time):
        self.tx_time = time

    def set_ack_time(self, time):
        self.ack_time = time



