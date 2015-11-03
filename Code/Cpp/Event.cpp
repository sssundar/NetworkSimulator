#include "Event.hpp"

void Event::set_completion_time(double time) {
    completion_time = time;
}

double Event::get_completion_time() {
    return completion_time;
}

void Event::event_action() {}