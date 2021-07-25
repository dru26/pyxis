#include "position.h"

// An 2D array storing the chance any given position will be blocked
class Map {
public:
    Map(int scale) : _scale(scale) {}
    // Accessors
    float get(Position p);
    void load();

private:
    Position transform(Position p)
    float _scale;
    float _grid;
};
