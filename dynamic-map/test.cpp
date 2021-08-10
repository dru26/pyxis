#include <iostream>
#include <assert.h>
#include <stdlib.h>

#include "map.h"
float PRECISION = 0.0001;

void basicTests() {
    // Scale of 1 cm
    ProbabilityMap map(100);
    // default map should be completely blank
    assert((map.width() == map.widtha() * 100) && (map.width() == 0));
    assert((map.height() == map.heighta() * 100) && (map.height() == 0));
    // Add a unit to the map and test it
    assert(map.get(Position(0, 0)) == 0);
    // there should be one tile existing
    assert((map.width() == map.widtha() * 100) && (map.width() == 100));
    assert((map.height() == map.heighta() * 100) && (map.height() == 100));
    // None of these should add a unit
    assert(map.get(Position(0, 0)) == 0);
    assert(map.get(Position(10, 0)) == 0);
    assert(map.get(Position(0, 10)) == 0);
    assert(map.get(Position(99, 0)) == 0);
    assert(map.get(Position(0, 99)) == 0);
    assert(map.get(Position(99, 99)) == 0);
    // there should still be one tile existing
    assert((map.width() == map.widtha() * 100) && (map.width() == 100));
    assert((map.height() == map.heighta() * 100) && (map.height() == 100));
    // This should add 1 tile
    assert(map.get(Position(100, 99)) == 0);
    assert((map.width() == map.widtha() * 100) && (map.width() == 200));
    assert((map.height() == map.heighta() * 100) && (map.height() == 100));
    // This should add 2 tiles
    assert(map.get(Position(100, 100)) == 0);
    assert((map.width() == map.widtha() * 100) && (map.width() == 200));
    assert((map.height() == map.heighta() * 100) && (map.height() == 200));
}

void continuityTest() {
    // Scale of 0.5 m
    ProbabilityMap map(2);
    // Add the gradient
    map.tell(Position(-1, 0), true);
    map.tell(Position(0, 0), true);
    map.tell(Position(0, 0), true);
    map.tell(Position(1, 0), true);
    map.tell(Position(1, 0), true);
    map.tell(Position(1, 0), true);
    map.tell(Position(-1, -1), true);
    map.tell(Position(-1, -1), true);
    map.tell(Position(0, -1), true);
    map.tell(Position(0, -1), true);
    map.tell(Position(0, -1), true);
    map.tell(Position(1, -1), true);
    map.tell(Position(1, -1), true);
    map.tell(Position(1, -1), true);
    map.tell(Position(1, -1), true);
    // Make sure the graident makes sense
    //std::cout << "get(-1,0): " << map.get(Position(-1, 0)) << std::endl;
    assert(abs(map.get(Position(-1, 0)) - pow(1.0 / 127.0, 2)) < PRECISION);
    assert(abs(map.get(Position(0, 0)) - pow(2.0 / 127.0, 2)) < PRECISION);
    assert(abs(map.get(Position(-1, -1)) - pow(2.0 / 127.0, 2)) < PRECISION);
    assert(abs(map.get(Position(1, 0)) - pow(3.0 / 127.0, 2)) < PRECISION);
    assert(abs(map.get(Position(0, -1)) - pow(3.0 / 127.0, 2)) < PRECISION);
    assert(abs(map.get(Position(1, -1)) - pow(4.0 / 127.0, 2)) < PRECISION);
    // Make sure the map size makes sense
    assert((map.width() == map.widtha() * 2) && (map.width() == 4));
    assert((map.height() == map.heighta() * 2) && (map.height() == 4));
}

void largeMapTests(int w, int h, int tests) {
    // Scale of 1 cm
    ProbabilityMap map(100);
    w = floor(w / 2);
    h = floor(h / 2);
    // This should add w x h tiles
    int wa, ha;
    wa = (w * 100) - 1;
    ha = (h * 100) - 1;
    assert(map.get(Position(wa, ha)) == 0);
    assert(map.get(Position(-wa, -ha)) == 0);
    assert((map.width() == map.widtha() * 100) && (map.widtha() == w * 2));
    assert((map.height() == map.heighta() * 100) && (map.heighta() == h * 2));
    // Set some tiles randomly
    std::vector<Position> random_pos;
    std::vector<int> random_int;
    int r, x, y;
    for (int i = 0; i < tests; i++) {
        r = (rand() % 128); // Rand between 0 and 127
        x = rand() % (wa + 1); // Rand between 0 and wa
        y = rand() % (ha + 1); // Rand between 0 and ha
        if (rand() % 2) { x = -x; }
        if (rand() % 2) { y = -y; }
        random_pos.push_back(Pos(x, y));
        random_int.push_back(r);
    } for (int i = 0; i < tests; i++) {
        //std::cout << "pos: " << random_pos[i] << std::endl;
        // Simulate multiple blockages or clearances
        for (int r = 0; r < random_int[i]; ++r) {
            map.tell(random_pos[i], true);
        }
        assert(abs(map.get(random_pos[i]) - pow(abs((float)random_int[i]) / 127.0, 2)) < PRECISION);
        // Clean those blockages out by doing the reverse
        for (int r = 0; r < random_int[i]; ++r) {
            map.tell(random_pos[i], false);
        }
        assert(map.get(random_pos[i]) == 0.0);
    }
    // While map.tell() can update the map size, it should not have in this test
    assert((map.width() == map.widtha() * 100) && (map.widtha() == w * 2));
    assert((map.height() == map.heighta() * 100) && (map.heighta() == h * 2));
}

int main() {
    loadTestMap("map.txt", 15);
    std::cout << "Loaded a p_map" << std::endl;
    // Run the basic test suite
    basicTests();
    std::cout << "Completed basic tests" << std::endl;
    // Run the continuity test
    continuityTest();

    // Run large maps with spot tests
    largeMapTests(100, 100, 200);/*
    std::cout << "Completed large map (100x100) test" << std::endl;
    largeMapTests(312, 2, 2000);
    std::cout << "Completed large map (312x2) test" << std::endl;
    largeMapTests(98, 2, 2000);
    std::cout << "Completed large map (98x2) test" << std::endl;
    largeMapTests(2, 98, 2000);
    std::cout << "Completed large map (2x98) test" << std::endl;
    largeMapTests(98, 98, 2000);
    std::cout << "Completed large map (98x98) test" << std::endl;
    largeMapTests(350, 400, 2000);
    std::cout << "Completed large map (350x400) test" << std::endl;
    largeMapTests(2, 2, 100000);
    std::cout << "Completed large map (2x2) test" << std::endl;*/
    return EXIT_SUCCESS;
}

int test(int n, float x) {
  return 1;
}
