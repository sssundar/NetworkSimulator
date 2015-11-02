#include "Packet.hpp"

using namespace std;

Packet::Packet (Node s, Node d, Flow f, std::string type, 
					int id, int bits) : 
					f(f), 
					source(s),
					destination(d),
					type(type),
					packet_id(id),
					bits(bits),
					acknowledged(false),
					in_transit(false),
					tx_time(-1),
					ack_time(-1) { 		
}

void Packet::set_tx_time (double t) {
	tx_time = t;
}

void Packet::set_ack_time (double t) {
	ack_time = t;
}

double Packet::get_RTT () {
	if (ack_time < 0) {
		return -1;
	} 
	else {
		return ack_time - tx_time;
	}
}

int Packet::bit_length() {
	return bits;
}

Node Packet::getCurrentDestination() {
	return destination;	
}

int Packet::get_id() {
	return packet_id;
}

std::string Packet::Packet::get_type() {
	return type;	
}

Flow Packet::get_flow_source() {
	return f;
}

bool Packet::was_acknowledged() {
	return acknowledged;
}

void Packet::acknowledge() {
	acknowledged = true;
	in_transit = false;
}

bool Packet::is_in_transit() {
	return in_transit;
}

void Packet::flag_in_transit() {
	in_transit = true;
}

void Packet::flag_timed_out () {
	in_transit = false;
}