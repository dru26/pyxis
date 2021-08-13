// To compile into .so files for bindings, run the following:
/*
g++ -o clib.o -c main.cpp
g++ -shared -o clib.so clib.o
*/

#include <utility>
#include <iostream>
#include <math.h>
#include <queue>
#include <set>
#include <vector>
#include <fstream>
#include <algorithm>
#include <unistd.h>

#include "position.h"
#include "map.h"
#include "path.h"

//typedef std::vector<Position> Path;
/*extern "C" void nextPosition(int* pos) {
  if (current.size() == 0) { return; }
  pos[0] = x(current.back());
  pos[1] = y(current.back());
  current.pop_back();
}
*/

const int WIDTH = 30;

void loadTestMap(ProbabilityMap& p_map, std::string path) {
  std::ifstream file(path);
  std::string line;
  //p_map = ProbabilityMap(scale);
  int y = 0;
  while (getline(file, line)) { // always check whether the file is open
    int x = 0;
    // Split by " " into the vector
    std::istringstream iss(line);
    while (iss) {
      std::string word;
      iss >> word;
      //std::cout << word << std::endl;
      if (word == "") { continue; }
      //p_map.tell(Position(x, y), true, stoi(word));
      //std::cout<<p_map.get(Position(x,y)) << std::endl;
      ++x;
    }
    ++y;
    //std::cout << line << std::endl; // pipe stream's content to standard output
  }
}

extern "C" void destructor(int* path) {
  free(path);
}

// implimentation of Dijkstra's algorithm
extern "C" int* getPath(int dest_x, int dest_y, int start_x, int start_y, int step, const char* path) {
    ProbabilityMap p_map(WIDTH / 2);

		// Transform the dest coords to a multiple of step from start
		dest_x = start_x + (round((dest_x - start_x) / step) * step);
		dest_y = start_y + (round((dest_y - start_y) / step) * step);



    loadTestMap(p_map, std::string(path));
    Position dest = Position(dest_x, dest_y);
    Position start = Position(start_x, start_y);

    //Postion start = map.getCurrentPosition();
    std::priority_queue<WeightedPath, std::vector<WeightedPath>, WeightedPathCompare> active;
    std::set<Position> finished;

    // Add the path from start to itself (cost of 0)
    WeightedPath new_path;
    new_path.push_back(start, p_map.get(start));
    active.push(new_path);

    WeightedPath min_path;
    Position cur_dest;
    while (active.size() != 0) {
        min_path = active.top();
        active.pop();
        cur_dest = min_path.get()[min_path.size() - 1];
        // If the min_path weight is negative, it is an invalid path
        if (min_path.weight() < 0) { continue; }
        // We have the minimum path, return it
        if (cur_dest == dest) {
          // This is a memory leak unless we deal with it
          int* return_path = (int*)calloc(1 + (min_path.size() * 2),  sizeof(int));
          for (int i = min_path.size() - 1; i >= 0; --i) {
            return_path[(i*2)+1] = x(min_path.get()[i]);
            return_path[(i*2)+2] = y(min_path.get()[i]);
          }
          // The first arg of the array has its length
          return_path[0] = min_path.size() * 2;
          return return_path;
        }
        // This potision has already been searched
        if (finished.find(cur_dest) != finished.end()) { continue; }
        //std::cout << cur_dest << " " << dest << std::endl;
        // Look for a potential additive path in each of the 4 cardinal directions
        for (int i = 0; i < 4; ++i) {
            if (finished.find(cur_dest + (DIRECTIONS[i] * step)) == finished.end()) {
                new_path = min_path;
                Position temp = cur_dest + (DIRECTIONS[i] * step);
                new_path.push_back(temp, p_map.getBotArea(temp));
                active.push(new_path);
            }
        }
        // Record this dest
        finished.insert(cur_dest);
/*
        std::cout << "====================" << std::endl;
        std::cout << min_path.size() << std::endl;
        for (int i = 0; i < min_path.size(); i++) {
          std::cout << min_path.get()[i] << std::endl;
        }*/
    }
    // No valid path was found
    return NULL;
}

int main() {
  getPath(21, 31, 0, 0, 5, "/home/thethiefofstars/Code/GitHub/pyxis/examples/maps/basic.txt");
}
