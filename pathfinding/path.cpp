#include <iostream>
#include <queue>
#include <set>
#include <vector>
#include <unistd.h>

#include "../dynamic-map/map.h"
#include "../dynamic-map/position.h"
#include "path.h"

Path getPath(ProbabilityMap p_map, Position dest);

Position DIRECTIONS[4] = {Pos(0, 1), Pos(1, 0), Pos(0, -1), Pos(-1, 0)};
Path EMPTY;

// implimentation of Dijkstra's algorithm
Path getPath(ProbabilityMap p_map, Position dest, Position start) {
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
        if (cur_dest == dest) { return min_path.get(); }
        // This potision has already been searched
        if (finished.find(cur_dest) != finished.end()) { continue; }
        //std::cout << cur_dest << " " << dest << std::endl;
        // Look for a potential additive path in each of the 4 cardinal directions
        for (int i = 0; i < 4; ++i) {
            if (finished.find(cur_dest + DIRECTIONS[i]) == finished.end()) {
                new_path = min_path;
                Position temp = cur_dest + DIRECTIONS[i];
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
        }
        usleep(1000 * 100);*/
    }
    // No valid path was found
    return EMPTY;
}
