#include <cstdlib>
#include "Packet.hpp"

class LinkQueue {

public:
    void LinkQueue(int capacity);
    bool can_enqueue();
    bool enqueue(Packet p);
    bool can_dequeue();
    Packet dequeue();

private:
    int head;
    int tail;
    int max_capacity;
    int current_length;
    std::vector<Packet *> buffer; 
};
