#ifndef EVENT_SIMULATOR_HEADER
#define EVENT_SIMULATOR_HEADER

#include <queue>
#include <vector>
#include "Event.hpp"
#include "Flow.hpp"

using namespace std;

class Event_Simulator {

public:
    void Event_Simulator(std::vector<Flow> f);
    void request_event(Event e);
    bool run_next_event();
    double get_current_time();

private:
    struct LessThanByTime();
    std::priority_queue<Event, std::vector<Event>, LessThanByTime> EventQueue;
    std::vector<Flow> flows;  
    bool are_flows_done(); 
    double time;
};

#endif