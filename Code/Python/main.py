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
	testCase0 = "input_test0.json"
	testCase1 = "input_test1.json"
	element_map = parser(testCase1)	

	''' Define Static Routing, Test Case 1, Ignoring Router 3 '''		
	r1_table = {"h1":"l0", "h2":"l1"}
	r2_table = {"h1":"l1", "h2":"l3"}
	r3_table = {"h1":"l2", "h2":"l4"}
	r4_table = {"h1":"l3", "h2":"l5"}
	element_map['r1'].static_routing(r1_table)
	element_map['r2'].static_routing(r2_table)
	element_map['r3'].static_routing(r3_table)
	element_map['r4'].static_routing(r4_table)

	sim = Event_Simulator(element_map)

	while (not sim.are_flows_done()):
		sim.run_next_event()

	print LOG + "Simulation Done"