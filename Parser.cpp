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
    std::vector<Node*> node_array;
    ifstream file ("input.txt");
    if (file.is_open()) {
        while (getline (file,line)) {
            std::vector<std::string> elems;
            elems = split(line,",");
            
            networkNode(elems, node_array);
            
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

networkNode(std::vector<std::string> elems, std::vector<Node*> node_array) {
    // IF HOST
    if (elems[0].compare("host") == 0) {
        if (search(elems[1], node_array) == -1) {
            node_array.push_back(host(elems[1]));   // INIT HOST with ID
        }
        for (int i = 2; i < elems.size(); i++) {
            if (search(elems[i], node_array) == -1) {
                node_array.push_back(link(elems[i]));
            }
        }
        
    }
    
    // IF ROUTER
    else if (elems[0].compare("router") == 0) {
        if (search(elems[1], node_array) == -1) {
            node_array.push_back(router(elems[1])); // INIT Router with ID
        }
        for (int i = 2; i < elems.size(); i++) {
            if (search(elems[i], node_array) == -1) {
                node_array.push_back(link(elems[i]));
            }
        }
    }
    
}

bool search(const std::string &s, std::vector<Node*> node_array){
    int exist = -1;
    for (int i = 0; i < node_array.size(); i++) {
        if (s.compare(node_array[i].getID()) == 0) {
            exist = i;
        }
    }
    return exist;
}
