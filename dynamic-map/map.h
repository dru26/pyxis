#ifndef dm_map
#define dm_map

#include <stdlib.h>

#include "position.h"

// An 2D array storing the chance any given position will be blocked
class ProbabilityMap {
public:
    ProbabilityMap(int scale) : _scale(scale) {}
    // Accessors
    // Retrieves the areal calculation of chance
    float get(Position p) { return rand() / (RAND_MAX + 1.); };
    void load();

private:
    Position transform(Position p);
    float _scale;
    float _grid;
};

#endif
