'''
#################################################################################
#################################################################################
#################################################################################
#################################################################################
## NEED TO TEST THIS, TO CONFIRM IT WORKS. NEED TO UNIT TEST ALL OF THIS CODE. ##
## Currently with Flow W = 100, seems broken 								   ##
#################################################################################
#################################################################################
#################################################################################
#################################################################################

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

# Data is parsed into triply nested dict with key-levels at link-id,
# measurement type, and link buffer direction. The final values
# are just [time (ms), buffer fractional occupancy (0-1)]
def handle_buffer_occupancy (datamap, datalog):	
	if datalog["measurement"] == "bufferoccupancy":			
		if not (datalog["linkid"] in datamap.keys()):								
			datamap[datalog["linkid"]] = {}					
		
		if not (datalog["measurement"] in datamap[datalog["linkid"]].keys()):			
			datamap[datalog["linkid"]][datalog["measurement"]] = {}

		if not (datalog["direction"] in datamap[datalog["linkid"]][datalog["measurement"]].keys()):	
			datamap[datalog["linkid"]][datalog["measurement"]][datalog["direction"]] = []		

		datamap[datalog["linkid"]][datalog["measurement"]][datalog["direction"]].append(\
			[	float(datalog["ms_globaltime"]), \
				float(datalog["fractional_buffer_occupancy"])\
				]\
				)		

# Breaks time into ms_window chunks and sums values within bins
def windowed_sum(times, values, ms_window):
	windowed_time = []
	windowed_values = []
	final_base_time = 0.0
	update_bin_flag = True
	k = 0
	while k  < len(times):
		if update_bin_flag is True:
			current_base_time = final_base_time		
			final_base_time = current_base_time + ms_window
			current_bin_time = final_base_time - float(ms_window)/2
			current_value_sum = 0.0			
			update_bin_flag = False

		if times[k] <= final_base_time:
			current_value_sum += values[k]			
			k += 1
		else:
			windowed_time.append(current_bin_time)						
			windowed_values.append(current_value_sum)			
			update_bin_flag = True
	return (windowed_time, windowed_values)

# Takes a time array (ms) and a values array measured at those times
# The values must be levels, not additive quantities. E.g. buffer occupancy.
# Returns the windowed time-average of the values array binned into 
# blocks of ms_window.

# Start at time 0, and for every event, keep track of forward inter-arrival t.
# Weight values by their time-to-next sample (level is constant till then)
# Divide by total ms_window to get value for that bin.
# Going forward, to the next window, remember the old value as the
# "starting state" (do NOT reset to 0)
def windowed_time_average(times, values, ms_window, initial_value):
	windowed_time = []
	windowed_values = []
	final_base_time = 0.0	
	update_bin_flag = True
	k = 0
	while k < len(times):

		if update_bin_flag is True:
			update_bin_flag = False
			current_base_time = final_base_time		
			final_base_time = current_base_time + ms_window
			current_bin_time = final_base_time - float(ms_window)/2
			
			if k == 0:
				current_value = initial_value							

			if times[k] <= final_base_time:
				current_value_time = times[k] - current_base_time
				current_sum = current_value * current_value_time
			else:
				current_value_time = ms_window
				current_sum = current_value * current_value_time
				windowed_time.append(current_bin_time)			
				windowed_values.append(current_sum/ms_window) 
				update_bin_flag = True
				continue			

		current_value = values[k]
		if (k+1) < len(times):
			nexteventtime = times[k+1]
		else:
			nexteventtime = final_base_time + 1

		if nexteventtime <= final_base_time:	
			current_value_time = times[k+1] - times[k]
			current_sum += current_value * current_value_time							
		else:			
			current_value_time = ms_window - (times[k] - current_base_time)
			current_sum += current_value * current_value_time			

			windowed_time.append(current_bin_time)			
			windowed_values.append(current_sum/ms_window)			
			update_bin_flag = True	
		k += 1						

	return (windowed_time, windowed_values)

'''
Confirm windowed time average function returns proper results 
for simple test cases:

Test1:
	ms_window = 10 ms, data = [[11ms, 1],[12ms,2],[13ms,1], [22ms,2]]
	initial_value = 0
Result Expected:
	t   v 
	5   0
	15  0*0.1+1*0.1+2*0.1+3*0.7 = 2.4
	25  1*0.2 + 2 * 0.8 = 1.8	
'''
def test_windowed_time_average ():
	# Test 1
	t, v = windowed_time_average([11,12,13,22], [1,2,1,2], 10, 0)
	te, ve = ([5,15,25], [0, 2.4, 1.8])
	for k in xrange(len(t)):
		print "t: %0.6f, te: %0.6f, v: %0.3f, ve: %0.3f" % (t[k],te[k],v[k],ve[k])

def example_plots_testcase1 (datamap, resultFilename):
	'''Time-Windowing, need window >> timescale of events (10x PROPDELAY for links...)'''
	ms_window = 100 

	if "l1" in datamap.keys():
		# Sample Plot, Test Case 1, Link 1 Link Rate		
		plt.subplot(2, 1, 1)
		ms_times = [val[0] for val in datamap["l1"]["linkrate"]]		
		mbit_transfers = [val[1] for val in datamap["l1"]["linkrate"]]				
		t, mb = windowed_sum(ms_times, mbit_transfers, ms_window)		
		t = np.array([val/1000 for val in t]) 				# s
		mbps = np.array([1000*val / ms_window for val in mb])  # Mbps		
		plt.plot(t, mbps,'kx-')
		plt.xlabel('Seconds')
		plt.ylabel('Mbps')
		plt.title('Test Case 1, Static Routing, Link 1 Rate & Left Buffer Occupancy')
		plt.grid(True)

		# Sample Plot, Test Case 1, Link 1 Left Buffer Occupancy		
		plt.subplot(2, 1, 2)
		ms_times = [val[0] for val in datamap["l1"]["bufferoccupancy"][constants.LTR]]
		frac_occupancy = [val[1] for val in datamap["l1"]["bufferoccupancy"][constants.LTR]]
		t, fo = windowed_time_average(ms_times, frac_occupancy, ms_window, 0.0) # buffers start empty
		t = np.array([val/1000 for val in t]) 				# s
		fo = np.array([100*val for val in fo])  			# %
		plt.plot(t, fo,'kx-')
		plt.xlabel('Seconds')
		plt.ylabel('% Occupancy')		
		plt.grid(True)		
	
		plt.savefig(resultFilename)
		# plt.show()

if __name__ == "__main__":
	# Temporary flag while I test time averaging & such for various logs
	local_function_testing_flag = True

	test_windowed_time_average()

	# Actual simulation & plotting
	if not local_function_testing_flag:
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
		 	 	 		handle_buffer_occupancy(eimtod, log)
		 	 	 		# ... other measurements to be supported later
				except ValueError:							
					pass
				except KeyError:				
					raise
		
		example_plots_testcase1(eimtod, resultFilename)

	sys.exit(0)