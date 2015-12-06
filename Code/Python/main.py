'''
Main Loop

Must be run in NetworkSimulator/Code/Python directiory.

Asks parser function to parse user input
Sends the generated network element map to event_simulator
Runs in a loop asking event_simulator to run_next_action until
all flow sources are done.

Logging is done by network elements to the STDOUT and we need to
cat this to a file in a bash script:
'''

from jsonparser import JSONParser
from event_simulator import Event_Simulator
import constants

class MainLoop ():
	def __init__ (self):
		pass

	def simulate (self, networkjson, tcp):	
		element_map = JSONParser(networkjson).parser(tcp)
		sim = Event_Simulator(element_map)

		while (not sim.are_flows_done()):
			sim.run_next_event()	

		return element_map