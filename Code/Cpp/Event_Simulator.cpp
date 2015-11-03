#include "Event_Simulator.hpp"

Event_Simulator::Event_Simulator(std::vector<Flow> f) {
    flows = f;
    time = 0    
}

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

double Event_Simulator::get_current_time() {
    return time;
}

bool Event_Simulator::are_flows_done() {
    bool flag = true;
    for (unsigned int i = 0; i < flows.size(); i++) {
		flag = flag & flows[i].is_done();
	}
	return flag;
}
