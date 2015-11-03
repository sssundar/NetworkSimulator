#include "Reporter.hpp"

public std::string get_id() {
    return ID;
}

public void log(std::string message) {
    printf("%s reports %s \n", get_id, message);
}
