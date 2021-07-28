#include <iostream>

#include "map.h"

void ProbabilityGrid::_make(unsigned int size) {
    std::cout << "grid?????" << std::endl;
    this->_size = size;
    // Create the probability grid
    this->_grid = (Chance**)calloc(size, sizeof(*(this->_grid)));
    for (int i = 0; i < size; ++i) {
        this->_grid[i] = (Chance*)calloc(size, sizeof(*(this->_grid[i])));
    }
}

ProbabilityGrid::~ProbabilityGrid() {
    std::cout << "grid" << std::endl;
    for (int i = 0; i < this->_size; ++i) {
        free(this->_grid[i]);
    }
    free(this->_grid);
}

float ProbabilityGrid::getProbability(const Position& p) {
    return (this->_grid[x(p)][y(p)]);
}

float ProbabilityGrid::getProbabilityArea(const Position& p1, const Position& p2) {
    float total = 0;
    float count = 0;

    // some code

    // Return the probability average for this area
    return (total / count) / 255;
}

float ProbabilityMap::get(const Position& p) {
    // Expand to the position if needed
    this->expand(p);
    // Advance to the proper position
    ProbabilityLayout::iterator itrx = this->_layout.begin();
    std::advance(itrx, (x(p) - this->_xmin) / this->_scale);
    std::list<ProbabilityGrid>::iterator itr = itrx->begin();
    std::advance(itr, (y(p) - this->_ymin) / this->_scale);
    // Return
    return itr->getProbability(translate(p));
    //return this->_grid[x(p)][y(p)];
}

Position ProbabilityMap::translate(const Position& p) {
    return Position(x(p) % this->_scale, y(p) % this->_scale);
}

// We can cut down the number of this->expand() calls to 4 by
// grouping this as a batch call
float ProbabilityMap::getArea(const Position& center, int range) {

}

// Assuming the position is invalid
void ProbabilityMap::expand(const Position& p) {
    // Expand in the y direction
    ProbabilityLayout::iterator itr;
    while (y(p) >= _ymax) {
        this->_default_grid_list.push_back(this->_default_grid);
        for (itr = this->_layout.begin(); itr != this->_layout.end(); ++itr) {
            itr->push_front(this->_default_grid);
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
