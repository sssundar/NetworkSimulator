#ifndef PACKET_HEADER
#define PACKET_HEADER

#include <cstdlib>
#include <string>
#include "Node.hpp"
#include "Flow.hpp"

using namespace std;

class Packet {

public: 	 
	Packet (Node s, Node d, Flow f, std::string type, int id, int bits);
	void set_tx_time (double t);
	void set_ack_time (double t);
	double get_RTT ();
	int bit_length();
	Node getCurrentDestination();
	int get_id();
	std::string get_type();
	Flow get_flow_source();
	bool was_acknowledged();
	void acknowledge();
	bool is_in_transit();
	void flag_in_transit();
	void flag_timed_out ();
	
private:
    double completion_time;
    Node source;
    Node destination;  		// host, router
	Flow f; 				// this packet's source

	std::string type; 		 	// ack, data for now
	int packet_id; 		// flow sink/source 
	int bits; 			// bit width of the packet
	
							// if this packet is from a source, was
							// it acknowledged yet by the sink?
	bool acknowledged = false; 
	bool in_transit = false;
	
							// for logging, flow control
	double tx_time;
	double ack_time; 	
};

#endif