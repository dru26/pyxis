#include <iostream>
#include <math.h>

#include "map.h"

void ProbabilityGrid::_make(unsigned int size) {
    this->_size = size;
    // Create the probability grid
    this->_grid = (Chance**)calloc(size, sizeof(*(this->_grid)));
    for (int i = 0; i < size; ++i) {
        this->_grid[i] = (Chance*)calloc(size, sizeof(*(this->_grid[i])));
    }
}

ProbabilityGrid::~ProbabilityGrid() {
    for (int i = 0; i < this->_size; ++i) {
        free(this->_grid[i]);
    }
    free(this->_grid);
}

float ProbabilityGrid::getProbability(const Position& p) {
    Position pos = p;
    if (x(p) < 0) {
        pos = Position(this->_size + x(pos), y(pos));
    } if (y(p) < 0) {
        pos = Position(x(pos), this->_size + y(pos));
    }
    return pow(((float)(int)this->_grid[x(pos)][y(pos)] / 127.0), 2);
}

void ProbabilityGrid::change(const Position& p, int delta) {
    Position pos = p;
    if (x(p) < 0) {
        pos = Position(this->_size + x(pos), y(pos));
    } if (y(p) < 0) {
        pos = Position(x(pos), this->_size + y(pos));
    }
    this->_grid[x(pos)][y(pos)] = (int)this->_grid[x(pos)][y(pos)] + delta;
    //std::cout << "CNG p: " << pos << ", val: " << (int)this->_grid[x(pos)][y(pos)] << "\n";
}

float ProbabilityGrid::getProbabilityArea() {
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

float ProbabilityMap::get(const Position& pos) {
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

Position ProbabilityMap::translate(const Position& p) {
    Position pos = p;
    if (x(p) < 0) {
        pos = Position(this->_scale + x(pos), y(pos));
    } if (y(p) < 0) {
        pos = Position(x(pos), this->_scale + y(pos));
    }
    return Position(x(pos) % this->_scale, y(pos) % this->_scale);
}

Position ProbabilityMap::trim(const Position& p, int scale) {
    return Position(floor((float)x(p) / this->_scale), floor((float)y(p) / this->_scale));
}

// Update a particular position's state
void ProbabilityMap::tell(const Position &pos, bool is_blocked) {
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
    if (is_blocked) {
        if (itr->getProbability(p) == 0.0) { return; }
        itr->change(p , -1);
    }
    // Increment
    else {
        if (itr->getProbability(p) == 1.0) { return; }
        itr->change(p , 1);
    }
}

// An temp. extremely inefficient function that can be optimized
float ProbabilityMap::getBotArea(const Position& center) {
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
void ProbabilityMap::expand(const Position& p) {
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
