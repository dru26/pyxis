#ifndef _map_h_
#define _map_h_

#include <stdlib.h>
#include <vector>
#include <list>

#include "position.h"

typedef unsigned char Chance;

// Grid with preallocated blocks
class ProbabilityGrid {
public:
    // Constructors, Copy, and Destructors
    // NOTE: The copy constructor is incomplete as a full copy constructor is not
    // needed. Simply calling the default _make() function is good enough for
    // our purposes
    ProbabilityGrid(unsigned int size) { this->_make(size); }
    ProbabilityGrid(const ProbabilityGrid& pg) { this->_make(pg._size); }
    ~ProbabilityGrid();
    // Accessors
    float getProbability() { return _chance; }
    float getProbability(const Position& p);
    float getProbabilityArea(const Position& p1, const Position& p2);
private:
    void _make(unsigned int size);
    Chance** _grid;
    unsigned int _size;
    float _chance;
};

typedef std::list<std::list<ProbabilityGrid>> ProbabilityLayout;

// An 2D array storing the chance any given position will be blocked
// The ideal size of a probability map is 1/2 the robot's width
class ProbabilityMap {
public:
    ProbabilityMap(unsigned int scale) : _scale(scale), _default_grid(scale) {}
    // Accessors
    // Retrieves the areal calculation of chance
    float get(const Position &p);
    float getArea(const Position& center, int range);
    int width() { return _xmax - _xmin; }
    int height() { return _ymax - _ymin; }
    int widtha() { return _layout.size(); }
    int heighta() { return _layout.size() ? _layout.front().size() : 0; }

private:
    void expand(const Position& p);
    Position translate(const Position& p);
    int _xmin = 0;
    int _xmax = 0;
    int _ymin = 0;
    int _ymax = 0;
    ProbabilityLayout _layout;
    ProbabilityGrid _default_grid;
    std::list<ProbabilityGrid> _default_grid_list;
    unsigned int _scale;
};

#endif
