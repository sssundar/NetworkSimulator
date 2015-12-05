'''
This function is run from the command line as either:

python visualize.py clean
	Clears the results directory
python visualize.py simulate
	Runs MainLoop on TestCase1 
python visualize.py plot
	Analyzes last simulation's data
	Outputs time-vs-value plots for debugging (no units yet)

Results (and raw measurements) are plotted to /Code/Python/results/
This directory is cleared after each run 
Currently, supported measurements include:
- link rate (mpbs)
- buffer occupancy (%)
- packet loss (packets)
- flow rate (Mbps)
- flow window size (packets)
- packet round trip time (ms)

But these are not so useful for debugging and it's easier to use testVis.py.
We'll be fixing this soon.

This script can and should be extended to handle parameter sweeps of MainLoop.

Last Revised by Sushant Sundaresh on 30 Nov 2015

References:
	http://matplotlib.org/examples/pylab_examples/simple_plot.html
	http://stackoverflow.com/questions/4675728/redirect-stdout-to-a-file-in-python
	http://stackoverflow.com/questions/14245227/python-reset-stdout-to-normal-after-previously-redirecting-it-to-a-file
'''
import constants

testCase = constants.TESTCASE1

import sys, os
import json
import matplotlib.pyplot as plt
import numpy as np
from main import MainLoop

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

def handle_flowrate (datamap, datalog):	
	if datalog["measurement"] == "flowrate":			
		if not (datalog["flowid"] in datamap.keys()):								
			datamap[datalog["flowid"]] = {}					
		
		if not (datalog["measurement"] in datamap[datalog["flowid"]].keys()):			
			datamap[datalog["flowid"]][datalog["measurement"]] = []		

		datamap[datalog["flowid"]][datalog["measurement"]].append(\
			[	float(datalog["ms_globaltime"]), \
				float(datalog["mbits_received_at_sink"])\
				]\
				)		

def handle_packet_loss (datamap, datalog):
	if datalog["measurement"] == "packetloss":	
		if not (datalog["flowid"] in datamap.keys()):								
			datamap[datalog["flowid"]] = {}	
		
		if not (datalog["measurement"] in datamap[datalog["flowid"]].keys()):			
			datamap[datalog["flowid"]][datalog["measurement"]] = []		

		# exactly one packet loss is reported each time
		datamap[datalog["flowid"]][datalog["measurement"]].append(\
			[	float(datalog["ms_globaltime"]), \
				float(1.0)\
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

def handle_flow_window (datamap, datalog):	
	if datalog["measurement"] == "windowsize":			
		if not (datalog["flowid"] in datamap.keys()):								
			datamap[datalog["flowid"]] = {}					
		
		if not (datalog["measurement"] in datamap[datalog["flowid"]].keys()):			
			datamap[datalog["flowid"]][datalog["measurement"]] = []

		datamap[datalog["flowid"]][datalog["measurement"]].append(\
			[	float(datalog["ms_globaltime"]), \
				float(datalog["windowsize"])\
				]\
				)		

def handle_flow_state (datamap, datalog):	
	if datalog["measurement"] == "flowstate":			
		if not (datalog["flowid"] in datamap.keys()):								
			datamap[datalog["flowid"]] = {}					
		
		if not (datalog["measurement"] in datamap[datalog["flowid"]].keys()):			
			datamap[datalog["flowid"]][datalog["measurement"]] = []

		datamap[datalog["flowid"]][datalog["measurement"]].append(\
			[	float(datalog["ms_globaltime"]), \
				float(datalog["state"])\
				]\
				)		

def handle_packets_outstanding (datamap, datalog):	
	if datalog["measurement"] == "outstandingpackets":			
		if not (datalog["flowid"] in datamap.keys()):								
			datamap[datalog["flowid"]] = {}					
		
		if not (datalog["measurement"] in datamap[datalog["flowid"]].keys()):			
			datamap[datalog["flowid"]][datalog["measurement"]] = []

		datamap[datalog["flowid"]][datalog["measurement"]].append(\
			[	float(datalog["ms_globaltime"]), \
				float(datalog["packets_out"]), \
				float(datalog["packets_left"]),\
				float(datalog["packets_in_transit"]),\
				float(datalog["packets_ackd"]),\
				float(datalog["total_packets"]),\
				]\
				)		

def handle_flow_reno_debug (datamap, datalog):	
	if datalog["measurement"] == "fullrenodebug":			
		if not (datalog["flowid"] in datamap.keys()):								
			datamap[datalog["flowid"]] = {}					
		
		if not (datalog["measurement"] in datamap[datalog["flowid"]].keys()):			
			datamap[datalog["flowid"]][datalog["measurement"]] = []

		datamap[datalog["flowid"]][datalog["measurement"]].append(\
			[	float(datalog["ms_globaltime"]), \
				datalog["SendReceive"],\
				int(datalog["whichPacket"]),\
				int(datalog["EPIT"]),\
				int(datalog["LPIA"]),\
				float(datalog["WS"]),\
				float(datalog["CAT"]),\
				float(datalog["STT"]),\
				int(datalog["L3P0"]),\
				int(datalog["L3P1"]),\
				int(datalog["L3P2"]),\
				datalog["TAF"],\
				datalog["DAF"],\
				datalog["SAF"],\
				int(datalog["State"]),\
				datalog["isTimeoutOccurring"] ])		

def handle_flow_fast_debug (datamap, datalog):	
	if datalog["measurement"] == "fullfastdebug":			
		if not (datalog["flowid"] in datamap.keys()):								
			datamap[datalog["flowid"]] = {}					
		
		if not (datalog["measurement"] in datamap[datalog["flowid"]].keys()):			
			datamap[datalog["flowid"]][datalog["measurement"]] = []

		datamap[datalog["flowid"]][datalog["measurement"]].append(\
			[	float(datalog["ms_globaltime"]), \
				datalog["SendReceive"],\
				int(datalog["whichPacket"]),\
				int(datalog["EPIT"]),\
				int(datalog["LPIA"]),\
				float(datalog["WS"]),\
				float(datalog["STT"]),\
				int(datalog["L3P0"]),\
				int(datalog["L3P1"]),\
				int(datalog["L3P2"]),\
				datalog["TAF"],\
				datalog["DAF"],\
				datalog["SAF"],\
				int(datalog["State"]),\
				datalog["FlagObserveRTT"],\
				datalog["FlagRampWS"],\
				datalog["isTimeoutOccurring"],\
				float(datalog["RTTmin"]),\
				float(datalog["RTTactEst"]),\
				int(datalog["ICAPTUW"]) ])		


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

Test1: First window is empty
	ms_window = 10 ms
	data = [[11ms, 1],[12ms,2],[13ms,1], [22ms,2]]
	initial_value = 0
Result Expected:
	t   v 
	5   0
	15  0*0.1 + 1*0.1 + 2*0.1 + 1*0.7 = 1.0
	25  1*0.2 + 2 * 0.8 = 1.8	
Test2: Second window is empty, non-zero initial value
	ms_window = 8 ms
	data = [[6ms, 2],[17ms,5],[23ms,1]]
	initial_value = 1
Result Expected:
	t 		v
	4 		0.75*1 + 0.25*2 = 1.25
	12 		2
	20	 	0.125*2 + 0.75*5 + 0.125*1 = 0.25 + 3.75 + 0.125 = 4.125

Last Verified on 14 Nov 2015, 11 PM, by Sushant Sundaresh
Added to unit tests
'''
def test_windowed_time_average ():
	names = ["Test1", "Test2"]
	args = [([11.,12.,13.,22.], [1.,2.,1.,2.], 10., 0.),\
			([6.,17.,23.],[2.,5.,1.],8.,1.)]
	exps = [([5.,15.,25.], [0., 1.0, 1.8]),\
			([4.,12.,20.],[1.25,2.,4.125])]

	passFlag = True
	for j in xrange(len(names)):
		# print names[j]
		t, v, w, i = args[j]
		te, ve = exps[j]
		ta, va = windowed_time_average(t,v,w,i)		

		for k in xrange(len(te)):		
			passFlag = passFlag and (ta[k] == te[k]) and (va[k] == ve[k])	
	return passFlag		

'''For ms_window time-windowing, need window >> timescale of events (10x PROPDELAY for links...)'''
def plot_linkrate (datamap, linkID, ms_window, axes):				
	if linkID in datamap.keys():						
		ms_times = [val[0] for val in datamap[linkID]["linkrate"]]		
		mbit_transfers = [val[1] for val in datamap[linkID]["linkrate"]]	
		t, mb = windowed_sum(ms_times, mbit_transfers, ms_window)		
		t = np.array([val/1000 for val in t]) 					# s
		mbps = np.array([1000*val / ms_window for val in mb])  	# Mbps		
		axes.plot(t, mbps,'kx-')		
		axes.set_ylabel("Link %s, Mbps" % linkID)		
		axes.grid(True)

'''For ms_window time-windowing, need window >> timescale of events (10x PROPDELAY for links...)'''
def plot_flowrate (datamap, flowID, ms_window, axes):				
	if flowID in datamap.keys():						
		ms_times = [val[0] for val in datamap[flowID]["flowrate"]]		
		mbit_transfers = [val[1] for val in datamap[flowID]["flowrate"]]	
		t, mb = windowed_sum(ms_times, mbit_transfers, ms_window)		
		t = np.array([val/1000 for val in t]) 					# s
		mbps = np.array([1000*val / ms_window for val in mb])  	# Mbps		
		axes.plot(t, mbps,'kx-')		
		axes.set_ylabel("Flow %s, Mbps" % flowID)		
		axes.grid(True)

# Direction of the form constants.RTL or LTR. 
# Element ID must be link string ID
# Will break if no data matches the specified element in your simulation logs
def plot_bufferoccupancy(datamap, linkID, direction, ms_window, axes):		
	if linkID in datamap.keys():						
		ms_times = [val[0] for val in datamap[linkID]["bufferoccupancy"][direction]]
		frac_occupancy = [val[1] for val in datamap[linkID]["bufferoccupancy"][direction]]
		t, fo = windowed_time_average(ms_times, frac_occupancy, ms_window, 0.0) # buffers start empty
		t = np.array([val/1000 for val in t]) 				# s
		fo = np.array([100*val for val in fo])  			# %
		axes.plot(t, fo,'kx-')		
		axes.set_ylabel("Link %s, Percent Occupancy" % linkID)		
		axes.grid(True)		

def plot_dynamic_flowwindowsize(datamap, flowID, ms_window, axes):		
	if flowID in datamap.keys():						
		ms_times = [val[0] for val in datamap[flowID]["windowsize"]]
		packet_windowsize = [val[1] for val in datamap[flowID]["windowsize"]]
		t, w = windowed_time_average(ms_times, packet_windowsize, ms_window, 1.0) # W=1 for dynamic TCP
		t = np.array([val/1000 for val in t]) 				# s
		w = np.array([val for val in w])  					# packets
		axes.plot(t, w,'kx-')		
		axes.set_ylabel("Flow %s, Window Size (packets)" % flowID)		
		axes.grid(True)		

def plot_packetloss (datamap, flowID, ms_window, axes):
	if flowID in datamap.keys():		
		if "packetloss" in datamap[flowID].keys():			
			ms_times = [val[0] for val in datamap[flowID]["packetloss"]]
			pack_lost = [val[1] for val in datamap[flowID]["packetloss"]]
			t, plost = windowed_sum(ms_times, pack_lost, ms_window) 
			t = np.array([val/1000 for val in t]) 				# s
			plost = np.array(plost) 					 		# packets
			axes.plot(t, plost,'kx-')						
			axes.set_ylabel("Flow %s Packets Lost" % flowID)
			plt.grid(True)		

if __name__ == "__main__":	
	measurementFilename = "results/measurements.txt"	

	if sys.argv[1] == "clean":				
		for f in os.listdir("results"):					
			print "Removing %s" % os.path.join('results', f)
			os.remove(os.path.join('results', f))

	if sys.argv[1] == "simulate":		
		# Run Main Loop on Test Case 1, temporarily redirecting STDOUT
		sys.stdout = open(measurementFilename, 'w')		
		MainLoop().simulate(testCase)
		sys.stdout = sys.__stdout__		
	
	if sys.argv[1] == "plot":
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
		 	 	 		handle_packet_loss(eimtod, log)
		 	 	 		handle_flowrate(eimtod, log)
		 	 	 		handle_flow_window(eimtod, log)
		 	 	 		handle_flow_state(eimtod, log)
		 	 	 		handle_packets_outstanding(eimtod, log)
		 	 	 		handle_flow_reno_debug(eimtod, log)
		 	 	 		handle_flow_fast_debug(eimtod, log)
		 	 	 		# others
				except ValueError:							
					pass
				except KeyError:				
					raise

		# Dump parsed measurements for visual debugging
		for element in eimtod.keys():
			for measurement in eimtod[element].keys():
				if isinstance(eimtod[element][measurement],dict):
					# more layers
					for dataclass in eimtod[element][measurement].keys():
						# actual data	
						with open(os.path.join('results',\
							"%s_%s_%s.txt"%(element,measurement,dataclass)),'w') as f:   					
							f.write("time\t\tvalue\n")
							for t,v in eimtod[element][measurement][dataclass]:
								f.write("%0.6e\t\t%0.6e\n"%(t,v))
				else:					
					# actual data
					with open(os.path.join('results',\
							"%s_%s.txt"%(element,measurement)),'w') as f:   					
						if measurement == "outstandingpackets":
							f.write("time\t\tout\t\tleft\t\tintransit\t\tackd\t\ttotal\n")
							for t,v1,v2,v3,v4,v5 in eimtod[element][measurement]:
								f.write("%0.6e\t\t%d\t\t%d\t\t%d\t\t%d\t\t%d\n"%(t,v1,v2,v3,v4,v5))
						elif measurement == "fullrenodebug":
							f.write("time\t\tReason\t\tPacketID\t\tEPIT\t\tLPIA\t\tWS\t\tCAT\t\tSTT\t\t[L3P0\t\tL3P1\t\tL3P2]\t\tTAF\t\tDAF\t\tSAF\t\tState\t\tTimeoutOccurred\n")
							for t,SendReceive,whichPacket,EPIT,LPIA,WS,CAT,STT,L3P0,L3P1,L3P2,TAF,DAF,SAF,State,TO in eimtod[element][measurement]:
								f.write("%0.6e\t\t%s\t\t%d\t\t%d\t\t%d\t\t%0.3e\t\t%0.3e\t\t%0.6e\t\t[%d\t\t%d\t\t%d]\t\t%s\t\t%s\t\t%s\t\t%d\t\t%s\n"%(t,SendReceive,whichPacket,EPIT,LPIA,WS,CAT,STT,L3P0,L3P1,L3P2,TAF,DAF,SAF,State,TO))
						elif measurement == "fullfastdebug":
							f.write("time\t\tReason\t\tPacketID\t\tEPIT\t\tLPIA\t\tWS\t\tSTT\t\t[L3P0\t\tL3P1\t\tL3P2]\t\tTAF\t\tDAF\t\tSAF\t\tState\t\tObserve\t\tRamp\t\tTimeoutOccurred\t\tRTTmin\t\tRTTAct\t\tPacketsTillCanChangeWS\n")
							for t,SendReceive,whichPacket,EPIT,LPIA,WS,STT,L3P0,L3P1,L3P2,TAF,DAF,SAF,State,FlagO,FlagR,TO,RTTm,RTTa,ICAPTUW in eimtod[element][measurement]:
								f.write("%0.6e\t\t%s\t\t%d\t\t%d\t\t%d\t\t%0.3e\t\t%0.6e\t\t[%d\t\t%d\t\t%d]\t\t%s\t\t%s\t\t%s\t\t%d\t\t%s\t\t%s\t\t%s\t\t%0.6e\t\t%0.6e\t\t%d\n"%(t,SendReceive,whichPacket,EPIT,LPIA,WS,STT,L3P0,L3P1,L3P2,TAF,DAF,SAF,State,FlagO,FlagR,TO,RTTm,RTTa,ICAPTUW))
						else:
							f.write("time\t\tvalue\n")
							for t,v in eimtod[element][measurement]:
								f.write("%0.6e\t\t%0.6e\n"%(t,v))

		ms_window = 100

		# link1_stats = plt.figure()
		# link1_linkrate_ax = link1_stats.add_subplot(211)
		# link1_leftbuffocc_ax = link1_stats.add_subplot(212)
		# plot_linkrate(eimtod, "l1", ms_window, link1_linkrate_ax)
		# plot_bufferoccupancy(eimtod, "l1", constants.LTR, ms_window, link1_leftbuffocc_ax)
		# link1_linkrate_ax.set_title("Link 1, Test Case 1 (Static Routing, TCP Reno)")
		# link1_leftbuffocc_ax.set_xlabel('Seconds')
		# link1_stats.savefig("results/temp_link1.jpeg")

		# flow1src_stats = plt.figure()
		# flow1src_packetloss_ax = flow1src_stats.add_subplot(311)
		# plot_packetloss(eimtod, "f1_src", ms_window, flow1src_packetloss_ax)
		# flow1src_packetloss_ax.set_title("Flow 1, Test Case 1 (Static Routing, TCP RENO)")
		# flow1src_flowrate_ax = flow1src_stats.add_subplot(312)
		# plot_flowrate(eimtod, "f1_dest", ms_window, flow1src_flowrate_ax)
		# flow1src_windowsize_ax = flow1src_stats.add_subplot(313)
		# plot_dynamic_flowwindowsize(eimtod, "f1_src", ms_window, flow1src_windowsize_ax)
		# flow1src_windowsize_ax.set_xlabel('Seconds')
		# flow1src_stats.savefig("results/temp_flow1.jpeg")

	sys.exit(0)