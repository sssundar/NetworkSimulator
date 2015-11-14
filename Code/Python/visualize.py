'''
This function runs the MainLoop and helps us visualize measurements output
by this loop to the STDOUT.

It temporarily redirects STDOUT to results/measurements.txt
then parses & plots the measurements it knows how to handle.

Plots will, for now, overwrite the local results/temp.jpeg 

Currently, supported measurements include:
- link rate (mpbs)

This script can and should be extended to handle parameter sweeps of MainLoop.

Last Revised by Sushant Sundaresh on 13 Nov 2015

References:
	http://matplotlib.org/examples/pylab_examples/simple_plot.html
	http://stackoverflow.com/questions/4675728/redirect-stdout-to-a-file-in-python
	http://stackoverflow.com/questions/14245227/python-reset-stdout-to-normal-after-previously-redirecting-it-to-a-file
'''

import sys
import json
import matplotlib.pyplot as plt
import numpy as np
from main import MainLoop
import constants

def handle_linkrate (datamap, datalog):	
	if datalog["measurement"] == "linkrate":			
		if not (datalog["linkid"] in datamap.keys()):								
			datamap[datalog["linkid"]] = {}					
		
		if not (datalog["measurement"] in datamap[datalog["linkid"]].keys()):			
			datamap[datalog["linkid"]][datalog["measurement"]] = []		

		datamap[datalog["linkid"]][datalog["measurement"]].append(\
			[	float(datalog["ms_globaltime"]), \
				float(datalog["mbits_propagated"])\
				]\
				)		

# Windows time in ms based on the ms_window
# Takes a time array and a values array measured at those times
# Returns the windowed average of the values array binned at ms_windows
def windowed_average(times, values, ms_window):
	windowed_time = []
	windowed_values = []
	final_base_time = 0.0
	update_bin_flag = True
	for k in xrange(len(times)):
		if update_bin_flag is True:
			current_base_time = final_base_time		
			final_base_time = current_base_time + ms_window
			current_bin_time = final_base_time - float(ms_window)/2
			current_value_sum = 0.0
			current_value_count = 0
			update_bin_flag = False

		if times[k] <= final_base_time:
			current_value_sum += values[k]
			current_value_count += 1
		else:
			windowed_time.append(current_bin_time)			
			if current_value_count > 0:
				windowed_values.append(current_value_sum/current_value_count)
			else:
				windowed_values.append(0.0)
			update_bin_flag = True
	return (windowed_time, windowed_values)

def example_linkrate_testcase1 (datamap):
		# Sample Plot, Test Case 1, Link 1 Link Rate Windowing at 300 ms
		ms_times = [val[0] for val in datamap["l1"]["linkrate"]]
		mbit_transfers = [val[1] for val in datamap["l1"]["linkrate"]]
		ms_window = 300

		t, mb = windowed_average(ms_times, mbit_transfers, ms_window)

		t = np.array([val/1000 for val in t]) 				# s
		mb = np.array([1000*val / ms_window for val in mb])  # Mbps

		plt.plot(t, mb,'kx-')
		plt.xlabel('Seconds')
		plt.ylabel('Average Mbps')
		plt.title('Test Case 1, Static Routing, Link 1 Rate')
		plt.grid(True)
		plt.savefig(resultFilename)
		plt.show()

if __name__ == "__main__":
	measurementFilename = "results/measurements.txt"
	resultFilename = "results/temp.jpeg"

	# Run Main Loop on Test Case 1, temporarily redirecting STDOUT
	sys.stdout = open(measurementFilename, 'w')
	MainLoop().simulate(constants.TESTCASE1)
	sys.stdout = sys.__stdout__

	# element id and measurement type to data map
	# keyed as ['l1']['linkrate']
	eimtod = {}

	# Parse out measurements from measurements file
	with open(measurementFilename) as m:   
		for line in m:
			try:
	 	 	 	log = json.loads(line)
	 	 	 	if log["logtype"] == "measurement":	 	 	 		
	 	 	 		handle_linkrate(eimtod, log)	
	 	 	 		# ... other measurements to be supported later
			except ValueError:
				# Remove these during debugging
				pass
			except KeyError:
				# Remove these during debugging
				raise
	
	# Try changing the hardcoded flow window size in flow.py, and running the 
	# simulation visualization bash script over and over. Can you explain it?
	example_linkrate_testcase1(eimtod)

	sys.exit(0)