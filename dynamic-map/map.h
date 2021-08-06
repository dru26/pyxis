#ifndef _map_h_
#define _map_h_

#include <stdlib.h>
#include <vector>
#include <list>

#include "position.h"

typedef signed char Chance;

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
    //float getProbabilityStashed() { return _chance; }
    float getProbability(const Position& p);
    float getProbabilityArea();
    // Modifiers
    void change(const Position& p, int delta);
private:
    void _make(unsigned int size);
    Chance** _grid;
    unsigned int _size;
    float _chance;
};

typedef std::list<std::list<ProbabilityGrid>> ProbabilityLayout;

// An 2D array storing the chance any given position will be blocked
// The ideal size of a probability map is 1/2 the robot's width
// THIS IS IMPORTANT, AS getBotArea() assumens this is the robots width and height
// Thus, scale == 0.5 * width
class ProbabilityMap {
public:
    ProbabilityMap(unsigned int scale) : _scale(scale), _default_grid(scale) {}
    // Accessors
    // Retrieves the areal calculation of chance
    float get(const Position &p);
    float getBotArea(const Position& center);
    void tell(const Position &p, bool is_blocked);
    int width() { return (_xmax - _xmin) * this->_scale; }
    int height() { return (_ymax - _ymin) * this->_scale; }
    int widtha() { return _layout.size(); }
    int heighta() { return _layout.size() ? _layout.front().size() : 0; }
    int _xmin = 0;
    int _xmax = 0;
    int _ymin = 0;
    int _ymax = 0;
private:
    void expand(const Position& p);
    Position translate(const Position& p);
    Position trim(const Position& p, int scale);

    ProbabilityLayout _layout;
    ProbabilityGrid _default_grid;
    std::list<ProbabilityGrid> _default_grid_list;
    int _scale;
};

#endif
