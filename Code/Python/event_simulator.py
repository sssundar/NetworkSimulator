'''
File: event_simulator.py

Description: our discrete event simulator, basically a priority queue

Initialization: 
 Takes a dictionary of network element objects (links, nodes, flows) indexed
 by unique ids

Operation:
 Keeps an internal heap of items like 
 (completion_time, unique_event_number, Event instance)
 to order Events by their non-unique completion time. 

Functions:
 get_element, takes a network id and returns the element object

Last Revised: 3 November 2015 by Sushant Sundaresh
                  created
              4 November 2015 by Sushant Sundaresh
                  set up priority queue & tested

Reference: https://docs.python.org/2/library/heapq.html

'''

import constants, itertools, flow, host, router
from heapq import *
from events import *

class Event_Simulator():

	network_elements = ""
	network_flow_sources = []

	global_time = 0.0    
	event_heap = []                       # list of entries arranged in a heap
	event_counter = itertools.count()     # unique sequence count

	def __init__(self, network_elements):                        
		self.event_heap = []                     
		self.event_counter = itertools.count()   
		self.global_time = 0.0    
		self.network_flow_sources = []

		# remember all network elements for this simulation               
		self.network_elements = network_elements
		# set global time to 0
		self.global_time = 0.0            

		# create host_array 
		host_array = []
		for el in self.network_elements.keys():
			if isinstance(self.network_elements[el], host.Host):
				host_array.append(el.get_id())
		for el in self.network_elements.keys():
			if isinstance(self.network_elements[el], router.Router):
				el.initalize_routing_table()
		# create timeout callback for routing.
		self.request_event(Start_Next_Routing_Cycle(constants.ROUTING_TABLE_UPDATE_PERIOD))

		# keep track of which flows are active sources - and start them
		# let each network element know we are the simulator
		for el in self.network_elements.keys():
			if isinstance(self.network_elements[el], flow.Data_Source):
				self.network_flow_sources.append(self.network_elements[el])		
				self.request_event(	Flow_Start(\
									el,\
									self.network_elements[el].get_start()\
									)\
								)
			self.network_elements[el].set_event_simulator(self)

	# takes a network id and returns the element object
	def get_element (self, network_id):
		try:
			return self.network_elements[network_id]
		except KeyError:
			raise

	def are_flows_done (self):
		result = 1
		for f in self.network_flow_sources:
			result = result & f.is_done()
		return result

	def get_current_time (self):
		return self.global_time

	def request_event(self, event):   
		
		# if isinstance(event,Handle_Packet_Propagation):
		# 	message = "a Handle_Packet_Propagation event was requested"
		# elif isinstance(event,Time_Out_Packet):
		# 	message = "a Time_Out_Packet event was requested"
		# elif isinstance(event,Handle_Packet_Transmission):
		# 	message = "a Handle_Packet_Transmission event was requested"
		# elif isinstance(event,Flow_Start):
		# 	message = "a Flow_Start event was requested"
		# print "\nEvent: %s" % message

		count = next(self.event_counter)
		entry = [event.get_completion_time(), count, event]    
		heappush(self.event_heap, entry)

	def run_next_event(self):
		'Pop the event with the lowest completion time from the heap.'    
		if self.event_heap:
			completion_time, count, event = heappop(self.event_heap)
			self.global_time = completion_time        
			event.event_action(self)
		else:
			raise KeyError('No more events to simulate')	