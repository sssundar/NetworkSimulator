#ifndef FLOW_HEADER
#define FLOW_HEADER

#include <cstdlib>
#include <string>
#include "Reporter.hpp"
#include "Node.hpp"
#include "Packet.hpp"
#include "CONSTANTS.hpp"
#include "Event_Simulator.hpp"

using namespace std;

class Flow : public Reporter {
	public:				
		Flow (std::string ID);
		void send(Packet p);
		void receive(Packet p);
		void start();
	
	 	void set_src(Node src); 
	 	void set_dst(Node dst); 
		void set_sim(Event_Simulator sim);
		void set_window (int window);

	private:
		int packet_window;
		Node src;
		Node dst;
		Event_Simulator sim;
};

#endif