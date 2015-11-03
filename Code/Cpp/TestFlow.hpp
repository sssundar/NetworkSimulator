#ifndef TESTFLOW_HEADER
#define TESTFLOW_HEADER

#include <cstdlib>
#include <string>
#include "Flow.hpp"
#include "Packet.hpp"

using namespace std;

class TestFlow : public Flow {
	public: 
		TestFlow ();
		TestFlow (std::string ID); 
};

#endif