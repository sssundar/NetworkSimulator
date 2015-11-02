#include <cstdlib>

class Event {

public:
    void event_action();
    void set_completion_time(double time);
    double get_completion_time();

private:
    double completion_time;
    
};
