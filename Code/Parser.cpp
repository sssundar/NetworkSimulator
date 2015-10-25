/*
(host,hostID,linkID)
(router,routerID,linkID,linkID)
(link,ID,nodeID,nodeID,rate(Mbps),delay(ms),buffer(KB))
(flow,ID,nodeID,nodeID,data(MB),start(s))

Map of nodes

Exist in Map?
    If No, create new node(ID)
    
    If Yes, add infoto(ID) 
    
*/

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <map>

using namespace std;

int main () {
    string line;
    std::map<std::string, Node*> node_map;
    ifstream file ("input.txt");
    if (file.is_open()) {
        while (getline (file,line)) {
            std::vector<std::string> elems;
            elems = split(line,",");
            
            node_map = networkNode(elems, node_map);
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


// Parser ignoring routers for now
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
