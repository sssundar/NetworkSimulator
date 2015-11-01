#ifndef NODE_HEADER
#define NODE_HEADER

#include <cstdlib>
#include "Reporter.hpp"
#include "Packet.hpp"

using namespace std;

class Node : public Reporter {

public:    
	virtual void receive (Packet p) = 0;
	
};

#endif
