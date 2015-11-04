# Link Code
# Sith Domrongkitchaiporn

from node import Node

# The class Node extends the class Reporter
class Link(Node):
    
    left = ""
    right = ""
    rate = -1 
    delay = -1
    buffer = -1
    left_buffer = []
    right_buffer = []
    sim = ""

    # Call Node initialization code, with the Node ID (required unique)
    # Initializes itself
    def __init__(self, identity, left, right, rate, delay, size):
        Node.__init__(self, identity)				
        self.left = left
        self.right = right
        self.rate = int(rate)
        self.delay = int(delay)
        self.buffer = int(size)
	
    def set_event_simulator (self, sim):
        self.sim = sim
        
    def get_left(self):
        return self.left
        
    def get_right(self):
        return self.right
        
    def get_rate(self):
        return self.rate
        
    def get_delay(self):
        return self.delay
        
    def get_buffer(self):
        return self.buffer