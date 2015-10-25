#include <queue>
#include <vector>
#include "event.hpp"

using namespace std;

class Event_Simulator {

public:
    void Event_Simulator(std::vector<flow> f);
    void request_event(Event e);
    bool run_next_event();
    double get_current_time();

private:
    std::priority_queue<Event, std::vector<Event>, LessThanByTime> EventQueue;
    std::vector<flow> flows;  
    struct LessThanBy();
    bool are_flows_done(); 
    double time;
};
