#ifndef NODE_HEADER
#define NODE_HEADER

#include <cstdlib>
#include "Reporter.hpp"
#include "Packet.hpp"

using namespace std;

class Packet;

class Node : public Reporter {

public:    
	void receive (Packet p);
	
};

#endif
