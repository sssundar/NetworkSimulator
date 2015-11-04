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