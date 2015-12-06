'''
This function is run from the command line as:

python visualize.py --testcase testcase.json --tcp [fast|vegas|reno]

Raw measurements are dumped to /results/all_measurements.txt
Parsed measurements and plots are stored in /Code/Python/results/[rawdata,plots]
These directories are cleared at the start of each run.

Currently, supported plots include:
- link rate (mpbs) 					
- buffer occupancy (%) 				
- packet loss (packets)				
- flow rate (Mbps) 					
- flow window size (packets) 		
- packet round trip time (ms)		

Plenty more measurements are made, so check out the actual data dumps.
Any plot for which data is reported is plotted. 

Time/Bin Averages are used when they improve understanding, but not when
they hide the inner workings of the network. In many cases events are
plotted directly. 

Last Revised by Sushant Sundaresh on 6 Dec 2015

References:
	http://matplotlib.org/examples/pylab_examples/simple_plot.html
	http://stackoverflow.com/questions/4675728/redirect-stdout-to-a-file-in-python
	http://stackoverflow.com/questions/14245227/python-reset-stdout-to-normal-after-previously-redirecting-it-to-a-file
	http://stackoverflow.com/questions/273192/in-python-check-if-a-directory-exists-and-create-it-if-necessary
'''
import constants

import sys, os
import json
import matplotlib.pyplot as plt
import numpy as np
from main import MainLoop

from link import Link
from flow import Flow, Data_Source
from tcp_reno_working import Working_Data_Source_TCP_RENO, Working_Data_Sink_TCP_RENO
from tcp_fast_working import Working_Data_Source_TCP_FAST
from tcp_vegas_working import Working_Data_Source_TCP_VEGAS


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
				datalog["isTimeoutOccurring"],\
				float(datalog["RTTactEst"]) ])		

def handle_flow_vegas_debug (datamap, datalog):	
	if datalog["measurement"] == "fullvegasdebug":			
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

def handle_flow_true_fast_debug (datamap, datalog):	
	if datalog["measurement"] == "fulltruefastdebug":			
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
				datalog["isTimeoutOccurring"],\
				float(datalog["RTTmin"]),\
				float(datalog["RTTmax"]),\
				float(datalog["RTTactEst"]) ])		


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

# Element ID must be link string ID
# Will break if no data matches the specified element in your simulation logs
def plot_bufferoccupancy(datamap, linkID, ms_window, axes):		
	if linkID in datamap.keys():		
		epsilon = 10**-7				
		rtl_ms_times = [val[0] for val in datamap[linkID]["bufferoccupancy"][constants.RTL]]
		ltr_ms_times = [val[0] for val in datamap[linkID]["bufferoccupancy"][constants.LTR]]
		rtl_frac_occupancy = [val[1] for val in datamap[linkID]["bufferoccupancy"][constants.RTL]]
		ltr_frac_occupancy = [val[1] for val in datamap[linkID]["bufferoccupancy"][constants.LTR]]
		rtl_t, rtl_fo = windowed_time_average(rtl_ms_times, rtl_frac_occupancy, ms_window, 0.0) # buffers start empty
		ltr_t, ltr_fo = windowed_time_average(ltr_ms_times, ltr_frac_occupancy, ms_window, 0.0) # buffers start empty
		rtl_t = np.array([val/1000 for val in rtl_t]) 				# s
		ltr_t = np.array([val/1000 for val in ltr_t]) 				# s
		rtl_fo = np.array([100*val+epsilon for val in rtl_fo])  			# %
		ltr_fo = np.array([100*val+epsilon for val in ltr_fo])  			# %
		l1, l2 = axes.semilogy(rtl_t, rtl_fo,'kx-',ltr_t,ltr_fo,'r.-')		
		axes.set_ylabel("Left|Right Buffer [%s Full]" % '%')
		axes.legend((l1,l2), ('Right-to-Left','Left-to-Right'), 'upper right')
		axes.grid(True)		

'''For ms_window time-windowing, need window >> timescale of events (10x PROPDELAY for links...)'''
def plot_linkrate (datamap, linkID, ms_window, axes):				
	if linkID in datamap.keys():						
		ms_times = [val[0] for val in datamap[linkID]["linkrate"]]		
		mbit_transfers = [val[1] for val in datamap[linkID]["linkrate"]]	
		t, mb = windowed_sum(ms_times, mbit_transfers, ms_window)		
		t = np.array([val/1000 for val in t]) 					# s
		mbps = np.array([1000*val / ms_window for val in mb])  	# Mbps		
		axes.plot(t, mbps,'k.-')		
		axes.set_ylabel("Mbps")		
		axes.grid(True)

'''For ms_window time-windowing, need window >> timescale of events (10x PROPDELAY for links...)'''
def plot_flow_rate (ms,mbits,label,ms_window,axes):				
	t, mb = windowed_sum(ms, mbits,ms_window)		
	t = np.array([val/1000 for val in t]) 					# s
	mbps = np.array([1000.0*val / ms_window for val in mb])  	# Mbps		
	axes.plot(t, mbps,'k.-')		
	axes.set_ylabel(label)		
	axes.grid(True)

# Usually there are too many of these points to integrate quickly
def plot_flow_window(ms,pkts,label,ms_window,axes):			
	t, w = windowed_time_average(ms, pkts, ms_window, 1.0) # W0=1 for all dynamic TCPs
	t = np.array([val/1000 for val in t]) 				# s
	w = np.array(w)					  					# packets
	axes.plot(t, w,'k.-')				
	axes.set_ylabel(label)				
	axes.grid(True)		

def plot_flow_loss (ms,pkts,label,ms_window,axes):
	t, plost = windowed_sum(ms, pkts, ms_window) 
	t = np.array([val/1000 for val in t]) 				# s
	plost = np.array(plost) 					 		# packets
	axes.plot(t, plost,'k.-')						
	axes.set_ylabel(label)
	plt.grid(True)		

# Usually there are too many of these points to integrate quickly
def plot_flow_delay (ms,ms_delay,label,ms_window,axes):	
	t, d = windowed_time_average(ms, ms_delay, ms_window, 0) # delay0=0 for our simulations
	t = np.array([val/1000 for val in t]) 				# s
	d = np.array(d) 							 		# ms	
	axes.plot(t, d,'k.-')						
	axes.set_ylabel(label)
	plt.grid(True)		

# Reference: http://stackoverflow.com/questions/273192/in-python-check-if-a-directory-exists-and-create-it-if-necessary
def ensure_dir(f):
	d = os.path.dirname(f)
	if not os.path.exists(d):
		os.makedirs(d)

if __name__ == "__main__":	
	if (len(sys.argv) == 2 and sys.argv[1] == "--help") or (len(sys.argv) != 5 or sys.argv[1] != "--testcase" or sys.argv[3] != "--tcp" or sys.argv[4] not in ["fast","vegas","reno"]):
		print "Usage: python visualize.py --testcase testcase.json --tcp [fast|vegas|reno]\n"		
		sys.exit(1)	

	measurementFilename = os.path.join('results','all_measurements.txt')
	testImageFilename = os.path.join(os.path.join('results','plots'), "test.jpeg")
	testRawDataFilename = os.path.join(os.path.join('results','rawdata'), "test.jpeg")
	ensure_dir(measurementFilename)
	ensure_dir(testImageFilename)
	ensure_dir(testRawDataFilename)

	testCase = sys.argv[2]
	tcp = sys.argv[4]

	for f in os.listdir("results"):							
		if not os.path.isdir(os.path.join('results',f)):
			print "Cleaning up... removing %s" % os.path.join('results', f)
			os.remove(os.path.join('results', f))
	for f in os.listdir(os.path.join('results','plots')):
		print "Cleaning up... removing %s" % os.path.join(os.path.join('results','plots'), f)
		os.remove(os.path.join(os.path.join('results','plots'), f))
	for f in os.listdir(os.path.join('results','rawdata')):
		print "Cleaning up... removing %s" % os.path.join(os.path.join('results','rawdata'), f)
		os.remove(os.path.join(os.path.join('results','rawdata'), f))

	print "Simulating network..."
	
	# Run Main Loop on Test Case 1, temporarily redirecting STDOUT
	# STDERR will report progress.
	sys.stdout = open(measurementFilename, 'w')		
	element_map = MainLoop().simulate(testCase,tcp)
	sys.stdout = sys.__stdout__		

	print "Done simulating..."
	print "Parsing results..."

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
	 	 	 		handle_flow_true_fast_debug(eimtod, log)
	 	 	 		handle_flow_vegas_debug(eimtod, log)
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
					with open(os.path.join(os.path.join('results','rawdata'),\
						"%s_%s_%s.txt"%(element,measurement,dataclass)),'w') as f:   					
						f.write("time\t\tvalue\n")
						for t,v in eimtod[element][measurement][dataclass]:
							f.write("%0.6e\t\t%0.6e\n"%(t,v))
			else:					
				# actual data. handle debug dumps separately 
				# these aren't just for debugging; they have really useful
				# data. we just aren't doing anything with most of it.
				with open(os.path.join(os.path.join('results','rawdata'),\
						"%s_%s.txt"%(element,measurement)),'w') as f:   					
					if measurement == "outstandingpackets":
						f.write("time\t\tout\t\tleft\t\tintransit\t\tackd\t\ttotal\n")
						for t,v1,v2,v3,v4,v5 in eimtod[element][measurement]:
							f.write("%0.6e\t\t%d\t\t%d\t\t%d\t\t%d\t\t%d\n"%(t,v1,v2,v3,v4,v5))
					elif measurement == "fullrenodebug":
						f.write("time\t\tReason\t\tPacketID\t\tEPIT\t\tLPIA\t\tWS\t\tCAT\t\tSTT\t\t[L3P0\t\tL3P1\t\tL3P2]\t\tTAF\t\tDAF\t\tSAF\t\tState\t\tTimeoutOccurred\t\tRTTEst\n")
						for t,SendReceive,whichPacket,EPIT,LPIA,WS,CAT,STT,L3P0,L3P1,L3P2,TAF,DAF,SAF,State,TO,RTTEst in eimtod[element][measurement]:
							f.write("%0.6e\t\t%s\t\t%d\t\t%d\t\t%d\t\t%0.3e\t\t%0.3e\t\t%0.6e\t\t[%d\t\t%d\t\t%d]\t\t%s\t\t%s\t\t%s\t\t%d\t\t%s\t\t%0.6e\n"%(t,SendReceive,whichPacket,EPIT,LPIA,WS,CAT,STT,L3P0,L3P1,L3P2,TAF,DAF,SAF,State,TO,RTTEst))
					elif measurement == "fullvegasdebug":
						f.write("time\t\tReason\t\tPacketID\t\tEPIT\t\tLPIA\t\tWS\t\tSTT\t\t[L3P0\t\tL3P1\t\tL3P2]\t\tTAF\t\tDAF\t\tSAF\t\tState\t\tObserve\t\tRamp\t\tTimeoutOccurred\t\tRTTmin\t\tRTTAct\t\tPacketsTillCanChangeWS\n")
						for t,SendReceive,whichPacket,EPIT,LPIA,WS,STT,L3P0,L3P1,L3P2,TAF,DAF,SAF,State,FlagO,FlagR,TO,RTTm,RTTa,ICAPTUW in eimtod[element][measurement]:
							f.write("%0.6e\t\t%s\t\t%d\t\t%d\t\t%d\t\t%0.3e\t\t%0.6e\t\t[%d\t\t%d\t\t%d]\t\t%s\t\t%s\t\t%s\t\t%d\t\t%s\t\t%s\t\t%s\t\t%0.6e\t\t%0.6e\t\t%d\n"%(t,SendReceive,whichPacket,EPIT,LPIA,WS,STT,L3P0,L3P1,L3P2,TAF,DAF,SAF,State,FlagO,FlagR,TO,RTTm,RTTa,ICAPTUW))
					elif measurement == "fulltruefastdebug":
						f.write("time\t\tReason\t\tPacketID\t\tEPIT\t\tLPIA\t\tWS\t\tSTT\t\t[L3P0\t\tL3P1\t\tL3P2]\t\tTAF\t\tDAF\t\tSAF\t\tTimeoutOccurred\t\tRTTmin\t\tRTTmax\t\tRTTAct\n")
						for t,SendReceive,whichPacket,EPIT,LPIA,WS,STT,L3P0,L3P1,L3P2,TAF,DAF,SAF,TO,RTTmi,RTTma,RTTac in eimtod[element][measurement]:
							f.write("%0.6e\t\t%s\t\t%d\t\t%d\t\t%d\t\t%0.3e\t\t%0.6e\t\t%d\t\t%d\t\t%d\t\t%s\t\t%s\t\t%s\t\t%s\t\t%0.6e\t\t%0.6e\t\t%0.6e\n"%(t,SendReceive,whichPacket,EPIT,LPIA,WS,STT,L3P0,L3P1,L3P2,TAF,DAF,SAF,TO,RTTmi,RTTma,RTTac))
					else:
						f.write("time\t\tvalue\n")
						for t,v in eimtod[element][measurement]:
							f.write("%0.6e\t\t%0.6e\n"%(t,v))

	print "Done parsing results..."
	print "Plotting results..."	

	'''
	Want to plot, for each network element for which these data are available:
	
	1 link rate (mpbs) 					
		1 bin-averaged	
	2 buffer occupancy (%) 			
		2 time-averaged	
	3 packet loss (packets)				
		3 bin-sum
	4 flow rate (Mbps) 					
		4 bin-averaged 
	5 flow window size (packets) 		
		5 time-averaged
	6 packet delay (ms)		
		6 event trace (solid line)

	All will be black lines, solid, or single points, dotted. 
	Plots will be totally separated.

	This code below is sensitive to LACK of data. It will likely break
	if any of the expected data for standard plots is not found
	in your simulation for some reason (weird locked routing, etc.)
	'''
	ms_window = constants.MS_WINDOW
	for (d,v) in element_map.items():
		if isinstance(v, Link):						
			myname = "Link %s"%v.get_id()			
			print "for %s..."%myname
			myid = v.get_id() 

			all_plots = plt.figure()

			linkrate_ax = all_plots.add_subplot(211)
			buffocc_ax = all_plots.add_subplot(212)			

			plot_linkrate(eimtod, myid, ms_window, linkrate_ax)
			plot_bufferoccupancy(eimtod, myid, ms_window, buffocc_ax)

			linkrate_ax.set_title("%s Trace"%myname)
			buffocc_ax.set_xlabel('Seconds')
			all_plots.savefig(os.path.join(os.path.join('results','plots'),"%s.jpeg"%myid))
			plt.close()

		elif isinstance(v,Data_Source):
			myid = v.get_id()
			myname = myid.split('_')[0]						
			print "for Flow %s..."%myname
			mysink = "%s_%s"%(myname,"dest") # see jsonparser.py						
			all_data = []

			pltCount = 0
			plot_functions = []			

			if isinstance(v, Working_Data_Source_TCP_RENO):
				# guaranteed to have this data 
				mydata = eimtod[myid]["fullrenodebug"]
				mytimes = [val[0] for val in mydata] # ms
				myWS = [val[5] for val in mydata]  	# packets
				myDelay = [val[16] for val in mydata] # ms
			elif isinstance(v, Working_Data_Source_TCP_VEGAS):			
				# guaranteed to have this data 
				mydata = eimtod[myid]["fullvegasdebug"]
				mytimes = [val[0] for val in mydata] # ms
				myWS = [val[5] for val in mydata]  	# packets
				myDelay = [val[18] for val in mydata] # ms						
			elif isinstance(v, Working_Data_Source_TCP_FAST):
				# guaranteed to have this data 				
				mydata = eimtod[myid]["fulltruefastdebug"]
				mytimes = [val[0] for val in mydata] # ms
				myWS = [val[5] for val in mydata]  	# packets
				myDelay = [val[16] for val in mydata] # ms				
			
			plot_functions.append(lambda ((ms,dat,label,ms_window,axes)): plot_flow_window(ms,dat,label,ms_window,axes))
			plot_functions.append(lambda ((ms,dat,label,ms_window,axes)): plot_flow_delay(ms,dat,label,ms_window,axes))
			
			all_data.append([mytimes,myWS,'Window (pkts)'])
			all_data.append([mytimes,myDelay,'RTT (ms)'])
			pltCount += 2

			pkLossFlag = False
			if "packetloss" in eimtod[mysink].keys():
				mydata = eimtod[mysink]["packetloss"]			
				myLossTime = [val[0] for val in mydata] # ms
				myLoss = [val[1] for val in mydata] # 0, 1				
				all_data.append([myLossTime,myLoss,"Loss (pkts)"])				
				pltCount += 1
				pkLossFlag = True
				plot_functions.append(lambda ((ms,dat,label,ms_window,axes)): plot_flow_loss(ms,dat,label,ms_window,axes))			
			
			if "flowrate" in eimtod[mysink].keys():
				mydata = eimtod[mysink]["flowrate"]	
				myRateTime = [val[0] for val in mydata] # ms
				myRate = [val[1] for val in mydata] # mbits    
				all_data.append([myRateTime,myRate,"Mbps"])
				pltCount += 1
				plot_functions.append(lambda ((ms,dat,label,ms_window,axes)): plot_flow_rate(ms,dat,label,ms_window,axes))

			all_plots = plt.figure()			
			myaxes = []
			flow_ws_ax = all_plots.add_subplot(pltCount,1,1)
			myaxes.append(flow_ws_ax)
			flow_delay_ax = all_plots.add_subplot(pltCount,1,2)			
			myaxes.append(flow_delay_ax)
			if pltCount == 3 and pkLossFlag:
				flow_loss_ax = all_plots.add_subplot(pltCount,1,3)			
				myaxes.append(flow_loss_ax)
			elif pltCount == 3:
				flow_rate_ax = all_plots.add_subplot(pltCount,1,3)		
				myaxes.append(flow_rate_ax)	
			elif pltCount > 3:
				flow_loss_ax = all_plots.add_subplot(pltCount,1,3)			
				myaxes.append(flow_loss_ax)
				flow_rate_ax = all_plots.add_subplot(pltCount,1,4)		
				myaxes.append(flow_rate_ax)	
			
			for m in xrange(pltCount):							
				plot_functions[m]((all_data[m][0],all_data[m][1],all_data[m][2],ms_window,myaxes[m]))

			myaxes[0].set_title("%s Trace"%myname)
			myaxes[len(myaxes)-1].set_xlabel('Seconds')
			all_plots.savefig(os.path.join(os.path.join('results','plots'),"%s.jpeg"%myname))
			plt.close()

		else:
			continue		

	
	print "Done plotting results..."
	print "Goodbye!"

	sys.exit(0)