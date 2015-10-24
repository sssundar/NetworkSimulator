#include "Reporter.hpp"

public string get_id() {
    return ID;
}

public void log(String message) {
    printf("%s reports %s \n", get_id, message);
}
