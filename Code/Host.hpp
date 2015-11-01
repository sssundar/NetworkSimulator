#ifndef HOST_HEADER
#define HOST_HEADER

#include <cstdlib>
#include <string>
#include "Reporter.hpp"
#include "Packet.hpp"
#include "Link.hpp"
#include "Flow.hpp"
#include "CONSTANTS.hpp"
#include "Node.hpp"

using namespace std;

class Host : public Node {	

	private:
		Link l;
		Flow f;

	public:
		Host (std::string ID);
		void set_link (Link l);
		void set_flow (Flow f);
		void receive (Packet p);
		void send (Packet p);
};

#endif