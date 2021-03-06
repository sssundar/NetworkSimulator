#include "Host.hpp"

using namespace std;

Host::Host () {}

Host::Host (std::string ID) {	
	this->ID = ID;
}

void Host::set_link (Link l) {
	this->l = l;	
}

void Host::set_flow (Flow f) {
	this->f = f;
}

void Host::receive (Packet p) {
	if (
		(p.get_type().compare(CONSTANTS::DATA_PACKET_ACKNOWLEDGEMENT_TYPE) == 0) 
		|| 
		(p.get_type().compare(CONSTANTS::DATA_PACKET_TYPE) == 0) 
		) 
 		f.receive(p);					
}

void Host::send (Packet p) {
	l.send(p, *this);
}
