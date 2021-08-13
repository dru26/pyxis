#ifndef _path_h_
#define _path_h_

#include <queue>
#include <set>
#include <vector>
#include <fstream>

#include "./position.h"

typedef std::vector<Position> Path;
static float LENGTH_FACTOR = 1.0 / 127.0;

const Position DIRECTIONS[4] = {Pos(0, 1), Pos(1, 0), Pos(0, -1), Pos(-1, 0)};

extern "C" bool isPathLoaded() {
  return true;
}

class WeightedPath {
public:
  WeightedPath() : _weight(0) {}
  void push_back(Position p, float w) {
    this->_path.push_back(p);
    // If this is FOR SURE blocked or it is
    if (w < 0 || w > 0.9) {
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
