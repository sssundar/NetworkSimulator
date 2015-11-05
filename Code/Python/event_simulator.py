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
'''

import constants

class Event_Simulator():

	network_elements = ""
	network_flow_sources = []

	global_time = 0.0    
	event_heap = []                       # list of entries arranged in a heap
	event_counter = itertools.count()     # unique sequence count

	def __init__(self, network_elements):                             
		# remember all network elements for this simulation               
		self.network_elements = network_elements
		# set global time to 0
		self.global_time = 0.0            
		# keep track of which flows are active sources
		for el in self.network_elements.keys():
			if isinstance(self.network_elements[el], Data_Source):
				network_flow_sources.append(self.network_elements[el])

	# takes a network id and returns the element object
	def get_element (self, network_id):
		try:
			return self.network_elements[network_id]
		except KeyError e:
			raise

	def are_flows_done (self):
		result = 1
		for f in network_flow_sources:
			result = result & f.is_done()
		return result

	def get_current_time (self):
		return global_time

	def request_event(self, event):    
		count = next(event_counter)
		entry = [event.get_completion_time(), count, event]    
		heappush(event_heap, entry)

	def run_next_event(self):
		'Pop the event with the lowest completion time from the heap.'    
		if event_heap:
			completion_time, count, event = heappop(event_heap)
			self.global_time = completion_time        
			event.event_action()
		else:
			raise KeyError('No more events to simulate')	