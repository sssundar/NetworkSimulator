#include "Flow.hpp"

using namespace std;

Flow::Flow (std::string ID) { this->ID = ID; }
void Flow::send(Packet p) {}
void Flow::receive(Packet p) {}
void Flow::start() {}
void Flow::set_src(Node src) { this->src = src; }	
void Flow::set_dst(Node dst) { this->dst = dst; }
void Flow::set_sim(Event_Simulator sim) {	this->sim = sim; }
void Flow::set_window (int window) { this->packet_window = window; }

