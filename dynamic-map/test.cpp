#include <iostream>
#include <assert.h>

#include "map.h"

int dmBasicTests() {
    // Scale of 1 cm
    ProbabilityMap map(100);
    // default map should be completely blank
    assert((map.width() == map.widtha()) && (map.width() == 0));
    assert((map.height() == map.heighta()) && (map.height() == 0));
    // Add a unit to the map and test it
    assert(map.get(Position(0, 0)) == 0);
}
