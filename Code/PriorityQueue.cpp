#include <queue>

using namespace std;

int main () {
    std::priority_queue<Event, std::vector<Event>, LessThanByTime> EventQueue;
    return 0;
}

struct LessThanByTime {
    bool operator()(const Event& lhs, const Event& rhs) const {
        return lhs.time < rhs.time;
    }
};
