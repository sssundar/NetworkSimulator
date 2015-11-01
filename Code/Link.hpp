#include <cstdlib>
#include <string>
#include "Reporter.hpp"

using namespace std;

class Link : public Reporter {
	public:
		Link (std::string ID);
	private:
		std:string ID;
}