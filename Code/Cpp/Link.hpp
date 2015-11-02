#ifndef LINK_HEADER
#define LINK_HEADER

#include <cstdlib>
#include <string>
#include "Reporter.hpp"

using namespace std;

class Link : public Reporter {
	public:
		Link ();
		Link (std::string ID);
	private:
		std::string ID;
};

#endif