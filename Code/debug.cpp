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

std::vector<std::string> split(const std::string &s, char delim) {
    std::vector<std::string> word;
    word = split(s, delim, word);
    return word;
}

/* Main Loop for Testing */

int main () {
    string line;
    ifstream file ("input.txt");
    if (file.is_open()) {
        while (getline (file,line)) {
            std::vector<std::string> elems;
            std::cout << line << "\n";
            elems = split(line,',');
            for (unsigned int i = 0; i < elems.size();i++) {
                std::cout << elems[i] << "\n";
            }
        }
    file.close();
    }

    else {
        cout << "Unable to open file"; 
    }
    
    return 0;
}
