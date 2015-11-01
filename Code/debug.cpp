#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <map>

using namespace std;

/* Helper Fuctions*/
std::vector<std::string> &split(const std::string &s, char delim, std::vector<std::string> &elems) {
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, delim)) {
        elems.push_back(item);
    }
    return elems;
}

std::vector<std::string> split(std::string &s, char delim) {
    std::vector<std::string> elems;
    split(s, delim, elems);
    return elems;
}

/* Main Loop for Testing */

int main () {
    string line;
    ifstream file ("input.txt");
    if (file.is_open()) {
        while (getline (file,line)) {
            std::vector<std::string> elems;
            elems = split(line,",");
        }
    file.close();
    }

    else {
        cout << "Unable to open file"; 
    }
    
    return 0;
}
