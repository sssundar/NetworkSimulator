'''
Main Loop

Must be run in NetworkSimulator/Code/Python directiory.

Asks parser function to parse user input
Sends the generated network element map to event_simulator
Runs in a loop asking event_simulator to run_next_action until
all flow sources are done.

Logging is done by network elements to the STDOUT and we need to
cat this to a file in a bash script:

python main.py > data.txt
python visualize.py data.txt
'''

from parser import *
from event_simulator import Event_Simulator
from constants import LOGHEADER as LOG

if __name__ == "__main__":
	testCase0 = "input.json"
	element_map = parser(testCase0)	
	sim = Event_Simulator(element_map)

	while (not sim.are_flows_done()):
		sim.run_next_event()

	print LOG + "Simulation Done"