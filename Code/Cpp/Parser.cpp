// Parser with Main Loop
// Sith Domrongkitchaiporn
// NetworkNode needs to be debugged

/*

*** Format for Input File ***
host,hostID,linkID)
router,routerID,linkID,linkID)
link,ID,nodeID,nodeID,rate(Mbps),delay(ms),buffer(KB)
flow,ID,nodeID,nodeID,data(MB),start(s)


Algorithm:
Create Node Map
Exist in Map?
    If No, create new node(ID)
    If Yes, add info to(ID) 
    
*/

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <map>

using namespace std;

/* 
// Ignoring Routers for now
// Has not been debugged
std::map<std::string, Node*> networkNode(std::vector<std::string> elems, std::map<std::string, Node*> node_map) {
    std::map<std::string, Node*>::iterator i;
    std::map<std::string, Node*>::iterator j;
    std::map<std::string, Node*>::iterator k;
    
    if (elems[0].compare("host") == 0) {
        i = node_map.find(elems[1]);
        if (i == node_map.end()) {
            node_map[elem[1]] = new host(elems[1]);
        }
        
        i = node_map.find(elems[1]);
        j = node_map.find(elems[2]);
        if (j == node_map.end()) {
            node_map[elem[2]] = new link(elems[2]);
        }
        i->second->addNode(j->second);
    }
    
    else if (elems[0].compare("link") == 0) {
        i = node_map.find(elems[1]);
        if (i == node_map.end()) {
            node_map[elem[1]] = new link(elems[1]);
        }
        
        i = node_map.find(elems[1]);
        j = node_map.find(elems[2]);
        k = node_map.find(elems[3]);
        i->second->addNode(j->second,k->second);
        i->addSpec(atoi(elems[4].c_str()), atoi(elems[5].c_str()), atoi(elems[6].c_str()))
    }
    
    else if (elems[0].compare("flow") == 0) {
        node_map[elem[1]] = new flow(elems[1]);
        
        i = node_map.find(elems[1]);
        j = node_map.find(elems[2]);
        k = node_map.find(elems[3]);
        i->second->addNode(j->second,k->second);
        i->secondaddSpec(atoi(elems[4].c_str()), atoi(elems[5].c_str()))
    }
    
    return node_map
}
*/

/* String Parsing
 * Splits a string by a delim
 * Works
 */
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
    split(s, delim, word);
    return word;
}

/* Main Loop */
int main () {
    string line;
    //std::map<std::string, Node*> node_map;
    ifstream file ("input.txt");
    if (file.is_open()) {
        while (getline (file,line)) {
            std::vector<std::string> elems;
            std::cout << line << "\n";
            elems = split(line,',');
            
            for (unsigned int i = 0; i < elems.size();i++) {
                std::cout << elems[i] << "\n";
            }
            
            //node_map = networkNode(elems, node_map);
        }
    file.close();
    }

    else {
        cout << "Unable to open file"; 
    }
    
    return 0;
}
