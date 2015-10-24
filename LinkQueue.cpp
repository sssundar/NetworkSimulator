#include "LinkQueue.hpp"

void LinkQueue::LinkQueue(int cap) {
    head = 0;
    tail = 0;
    max_capacity = n;
    current_length = tail - head;  // What is this?
    std::vector<Packet *> buffer (max_capacity);
}

// returns true if could enqueue, false if queue is full
bool LinkQueue::can_enqueue() {
    return (max_capacity < current_length);
}

bool LinkQueue::can_dequeue() {
    return (current_length > 0);
}

bool LinkQueue::enqueue(Packet* p) {
    bool flag = false;
    
    if (can_enqueue()) {
        buffer[tail] = p*;
        tail++;
        if (tail == max_capacity) {
            tail = 0;
        }
        current_length++;
        flag = true;
    }
    return flag;
}

Packet LinkQueue::dequeue() {
    Packet popped = buffer[head];
    head++;
    if (head == max_capacity) {
        head = 0;
    }
    current_length--;
    return popped;
}
