#include <iostream>

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
    //std::cout << "        < p: " << pos << ", val: " << (int)this->_grid[x(pos)][y(pos)] << "\n";
    //std::cout << "pos: "<< pos << std::endl;
    return ((float)(int)this->_grid[x(pos)][y(pos)] / 127.0);
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

float ProbabilityGrid::getProbabilityArea(const Position& p1, const Position& p2) {
    float total = 0;
    float count = 0;

    // some code

    // Return the probability average for this area
    return (total / count) / 127.0;
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
    //std::cout << "GET\n";
    //std::cout << "  > grid: "<< p << ", pos" << translate(pos) << ", act: " << pos << "\n";
    //std::cout << "     > p: " << itr->getProbability(translate(pos))<< "\n";
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
    //std::cout << "trim pos: " << p <<"\n";
    //std::cout << "floor trim: "<< (float)x(p) / this->_scale << "\n";
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
    //std::cout << "TELL\n";
    //std::cout << "  > grid: "<< p << ", pos" << translate(pos) << ", act: " << pos << "\n";
    //std::cout << "     > p: " << itr->getProbability(translate(pos))<< "\n";
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

// We can trim down the number of this->expand() calls to 4 by
// grouping this as a batch call
float ProbabilityMap::getArea(const Position& center, int range) {

}

// Assuming the position is invalid
void ProbabilityMap::expand(const Position& p) {

    // Expand in the y direction
    //std::cout << "start" << p <<"\n";
    ProbabilityLayout::iterator itr;
    while (y(p) >= _ymax) {
        //std::cout <<"_ymax\n";
        this->_default_grid_list.push_back(this->_default_grid);
        for (itr = this->_layout.begin(); itr != this->_layout.end(); ++itr) {
            itr->push_back(this->_default_grid);
        }
        ++this->_ymax;
    }
    while (y(p) < _ymin) {
        //std::cout <<"_ymin\n";
        this->_default_grid_list.push_back(this->_default_grid);
        for (itr = this->_layout.begin(); itr != this->_layout.end(); ++itr) {
            itr->push_front(this->_default_grid);
        }

        --this->_ymin;

    }
    // Expand in the x max direction
    while (x(p) >= _xmax) {
        //std::cout <<"_xmax\n";
        this->_layout.push_back(this->_default_grid_list);
        ++this->_xmax;
    }
    while (x(p) < _xmin) {
        //std::cout <<"_xmin\n";
        this->_layout.push_front(this->_default_grid_list);
        --this->_xmin;
    }
    //std::cout << "end\n";
}
