#include <cstdlib>
#include <string>
#include "Reporter.hpp"
#include "Node.hpp"
#include "Packet.hpp"
#include "Event_Simulator.hpp"
#include "CONSTANTS.hpp"
#include "Testflow.hpp"

using namespace std;

TestFlow (std::string ID) : Flow(ID) {}
void TestFlow::send(Packet p) {}
void TestFlow::receive(Packet p) {}
void TestFlow::start() {}