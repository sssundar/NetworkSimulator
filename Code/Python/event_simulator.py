# File: event_simulator.py
#
# Description: our discrete event simulator, basically a priority queue
# 
# Initialization: 
#  Takes a dictionary of network element objects (links, nodes, flows) indexed
#  by unique ids
#
# Functions:
#  get_element, takes a network id and returns the element object
#
# Last Revised: 3 November 2015 by Sushant Sundaresh
#                   created

import constants

class Event_Simulator():

    network_elements = ""
    network_flow_sources = []
    
    global_time = 0.0
    enqueue_counter = 0

    def __init__(self, network_elements):                             
        # remember all network elements for this simulation               
        self.network_elements = network_elements
        # keep track of which flows are active sources
        for el in self.network_elements.keys():
            if self.network_elements[el].get_element_type() == constants.FLOW_DATA_SOURCE_ELEMENT:
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


pq = []                         # list of entries arranged in a heap
entry_finder = {}               # mapping of tasks to entries
REMOVED = '<removed-task>'      # placeholder for a removed task
counter = itertools.count()     # unique sequence count

def add_task(task, priority=0):
    'Add a new task or update the priority of an existing task'
    if task in entry_finder:
        remove_task(task)
    count = next(counter)
    entry = [priority, count, task]
    entry_finder[task] = entry
    heappush(pq, entry)

def remove_task(task):
    'Mark an existing task as REMOVED.  Raise KeyError if not found.'
    entry = entry_finder.pop(task)
    entry[-1] = REMOVED

def pop_task():
    'Remove and return the lowest priority task. Raise KeyError if empty.'
    while pq:
        priority, count, task = heappop(pq)
        if task is not REMOVED:
            del entry_finder[task]
            return task
    raise KeyError('pop from an empty priority queue')


class LessThanByTime
{
    public:
        bool operator() (Event lhs, Event rhs) {
            return lhs.get_completion_time() < rhs.get_completion_time();
        }
};

class Event_Simulator {

public:
    Event_Simulator(std::vector<Flow> f);
    void request_event(Event e);
    bool run_next_event();

private:    
    std::priority_queue<Event, std::vector<Event>, LessThanByTime> EventQueue;
    std::vector<Flow> flows;  
    
    
};


void Event_Simulator::request_event(Event e)() {
    EventQueue.push(e);
}

bool Event_Simulator::run_next_event() {
    
    if (EventQueue.empty()){
        return false;
    }
    
    Event e;
    e = EventQueue.pop();
    e.event_action();
    time = e.get_completion_time();
}
