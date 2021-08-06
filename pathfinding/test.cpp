#include <iostream>
#include <assert.h>
#include <stdlib.h>

#include "../dynamic-map/position.h"
#include "../dynamic-map/map.h"
#include "path.h"

void print(Path p) {
  for (int i = 0; i < p.size(); i++) {
    std::cout << p[i] << std::endl;
  }
}



void linearPaths() {
  ProbabilityMap map(100);
  Position a(0, 0);
  Position b(-10200, -23);
  Path path = getPath(map, a, b);
  print(path);
}

void calibration() {

}

int main() {
    // Run the basic test suite
    linearPaths();
    std::cout << "Completed basic tests" << std::endl;
    return EXIT_SUCCESS;
}
