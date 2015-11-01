#include <cstdlib>
#include <string>
#include "Reporter.hpp"
#include "Node.hpp"
#include "Packet.hpp"
#include "Event_Simulator.hpp"
#include "CONSTANTS.hpp"
#include "Flow.hpp"

using namespace std;

Flow (std::string ID) { this->ID = ID; }
void Flow::set_src(Node src) { this->src = src; }	
void Flow::set_dst(Node dst) { this->dst = dst; }
void Flow::set_sim(Event_Simulator sim) {	this->sim = sim; }
void Flow::set_window (int window) { this->packet_window = window; }

