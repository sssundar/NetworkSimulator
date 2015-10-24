/*(host,hostID,linkID)
(router,routerID,linkID,linkID)
(link,ID,nodeID,nodeID,rate(Mbps),delay(ms),buffer(KB))
(flow,ID,nodeID,nodeID,data(MB),start(s))

Vector of nodes

Exist in Vector?
    If No, create new node(ID)
    
    If Yes, add infoto(ID) 
    
*/

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>

using namespace std;

int main () {
    string line;
    ifstream file ("input.txt");
    if (file.is_open()) {
        while (getline (file,line)) {
            std::vector<std::string> elems;
            elems = split(line,",");
            
            networkNode(elems);
            
        }
    file.close();
    }

    else {
        cout << "Unable to open file"; 
    }
    
    return 0;
}

std::vector<std::string> &split(const std::string &s, char delim, std::vector<std::string> &elems) {
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, delim)) {
        elems.push_back(item);
    }
    return elems;
}

std::vector<std::string> split(const std::string &s, char delim) {
    std::vector<std::string> elems;
    split(s, delim, elems);
    return elems;
}
