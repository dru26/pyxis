#ifndef _map_h_
#define _map_h_

#include <stdlib.h>
#include <vector>
#include <list>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <iterator>

#include "position.h"

typedef signed char Chance;

extern "C" bool isMapLoaded() {
  return true;
}

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
    void tell(const Position &p, bool is_blocked, int count = 1);
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

// Bot is 30x30cm, so we use a scale of 15cm for optimizations
inline void ProbabilityGrid::_make(unsigned int size) {
    this->_size = size;
    // Create the probability grid
    this->_grid = (Chance**)calloc(size, sizeof(*(this->_grid)));
    for (int i = 0; i < size; ++i) {
        this->_grid[i] = (Chance*)calloc(size, sizeof(*(this->_grid[i])));
    }
}

inline ProbabilityGrid::~ProbabilityGrid() {
    for (int i = 0; i < this->_size; ++i) {
      free(this->_grid[i]);
    }
    free(this->_grid);
}

inline float ProbabilityGrid::getProbability(const Position& p) {
    Position pos = p;
    if (x(p) < 0) {
        pos = Position(this->_size + x(pos), y(pos));
    } if (y(p) < 0) {
        pos = Position(x(pos), this->_size + y(pos));
    }
    return pow(((float)(int)this->_grid[x(pos)][y(pos)] / 127.0), 2);
}

inline void ProbabilityGrid::change(const Position& p, int delta) {
    Position pos = p;
    if (x(p) < 0) {
        pos = Position(this->_size + x(pos), y(pos));
    } if (y(p) < 0) {
        pos = Position(x(pos), this->_size + y(pos));
    }
    this->_grid[x(pos)][y(pos)] = (int)this->_grid[x(pos)][y(pos)] + delta;
    //std::cout << "CNG p: " << pos << ", val: " << (int)this->_grid[x(pos)][y(pos)] << "\n";
}

inline float ProbabilityGrid::getProbabilityArea() {
    float total = 0;
    float count = this->_size * this->_size;
    float p;
    // Add the entire area
    for (int i = 0; i < this->_size; i++) {
      for (int j = 0; j < this->_size; i++) {
        p = getProbability(Position(i, j));
        if (p < 0) { return -1; }
        total += p;
      }
    }
    // Return the probability average for this area
    return (total / count);
}

inline float ProbabilityMap::get(const Position& pos) {
    // Expand to the position if needed and change the scope of p
    Position p = trim(pos, this->_scale);
    this->expand(p);
    // Advance to the proper position
    ProbabilityLayout::iterator itrx = this->_layout.begin();
    std::advance(itrx, x(p) + abs(this->_xmin));
    std::list<ProbabilityGrid>::iterator itr = itrx->begin();
    std::advance(itr, y(p) + abs(this->_ymin));
    // Change the scope of p and return
    return itr->getProbability(translate(pos));
}

inline Position ProbabilityMap::translate(const Position& p) {
    Position pos = p;
    if (x(p) < 0) {
        pos = Position(this->_scale + x(pos), y(pos));
    } if (y(p) < 0) {
        pos = Position(x(pos), this->_scale + y(pos));
    }
    return Position(x(pos) % this->_scale, y(pos) % this->_scale);
}

inline Position ProbabilityMap::trim(const Position& p, int scale) {
    return Position(floor((float)x(p) / this->_scale), floor((float)y(p) / this->_scale));
}

// Update a particular position's state
inline void ProbabilityMap::tell(const Position &pos, bool is_blocked, int count) {
    // Expand to the position if needed and change the scope of p
    Position p = trim(pos, this->_scale);
    this->expand(p);
    // Advance to the proper position
    ProbabilityLayout::iterator itrx = this->_layout.begin();
    std::advance(itrx, x(p) + abs(this->_xmin));
    std::list<ProbabilityGrid>::iterator itr = itrx->begin();
    std::advance(itr, y(p) + abs(this->_ymin));
    // Change the scope of p
    p = translate(pos);
    // Decrement
    if (!is_blocked) {
        if (itr->getProbability(p) == 0.0) { return; }
        itr->change(p , -count);
    }
    // Increment
    else {
        if (itr->getProbability(p) == 1.0) { return; }
        itr->change(p , count);
    }
}

// An temp. extremely inefficient function that can be optimized
inline float ProbabilityMap::getBotArea(const Position& center) {
  // Get the bounds
  int xmax = x(center) + this->_scale;
  int ymax = y(center) + this->_scale;
  int xmin = x(center) + this->_scale;
  int ymin = y(center) + this->_scale;
  // Setup vars
  float total = 0;
  float count = (this->_scale * 2) * (this->_scale * 2);
  float p;
  // Loop over the area and call get()
  for (int x = xmin; x < xmax; x++) {
    for (int y = ymin; y < ymax; y++) {
      p = this->get(Position(x, y));
      if (p < 0) { return -1; }
      total += p;
    }
  }
  return (total / count);
}

// Assuming the position is invalid
inline void ProbabilityMap::expand(const Position& p) {
    // Expand in the y direction
    ProbabilityLayout::iterator itr;
    while (y(p) >= _ymax) {
        this->_default_grid_list.push_back(this->_default_grid);
        for (itr = this->_layout.begin(); itr != this->_layout.end(); ++itr) {
            itr->push_back(this->_default_grid);
        }
        ++this->_ymax;
    }
    while (y(p) < _ymin) {
        this->_default_grid_list.push_back(this->_default_grid);
        for (itr = this->_layout.begin(); itr != this->_layout.end(); ++itr) {
            itr->push_front(this->_default_grid);
        }

        --this->_ymin;

    }
    // Expand in the x max direction
    while (x(p) >= _xmax) {
        this->_layout.push_back(this->_default_grid_list);
        ++this->_xmax;
    }
    while (x(p) < _xmin) {
        this->_layout.push_front(this->_default_grid_list);
        --this->_xmin;
    }
}



#endif
