#ifndef _path_h_
#define _path_h_

#include "../dynamic-map/position.h"

typedef std::vector<Position> Path;
static float LENGTH_FACTOR = 1.0 / 127.0;


Path getPath(ProbabilityMap p_map, Position dest, Position start);

class WeightedPath {
public:


    WeightedPath() : _weight(0) {}
    void push_back(Position p, float w) {
      this->_path.push_back(p);
      if (w < 0) {
        this->_weight = -1;
        return;
      }
      this->_weight += w;
    }
    int size() const { return this->_path.size(); }
    float weight() const { return (LENGTH_FACTOR * (float)this->size()) + this->_weight; }
    Path get() { return this->_path; }
    void operator=(const WeightedPath& rhs) { this->_path = rhs._path; this->_weight = rhs._weight; }
private:
    Path _path;
    float _weight;
};

class WeightedPathCompare {
public:
    bool operator() (const WeightedPath &a, const WeightedPath &b) {
        return a.weight() > b.weight();
    }
};

#endif
