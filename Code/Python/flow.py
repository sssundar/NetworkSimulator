# flow Code
# Sith Domrongkitchaiporn

from reporter import Reporter

# This class only extends Reporter Class
class flow(Reporter):
    source = ""
    dest = ""
    size = -1
    start =  -1
    sim = ""

    # Call Node initialization code, with the Node ID (required unique)
    # Initializes itself
    def __init__(self, identity, src, sink, size, start):
        Reporter.__init__(self, ID)
        self.source = src
        self.dest = sink
        self.size = int(size)
        self.start = int(start)

    def set_event_simulator (self, sim):
        self.sim = sim