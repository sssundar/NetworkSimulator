#ifndef TESTFLOW_HEADER
#define TESTFLOW_HEADER

#include <cstdlib>
#include <string>
#include "Flow.hpp"
#include "Packet.hpp"

using namespace std;

class TestFlow : public Flow {
	public: 
		TestFlow (std::string ID); 
		void send(Packet p) = 0;
		void receive(Packet p) = 0;
		void start() = 0;
};

#endif