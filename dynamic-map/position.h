#ifndef _position_h_
#define _position_h_

#include <iostream>
#include <math.h>

typedef std::pair<int, int> Position;

extern "C" bool isPositionLoaded() {
  return true;
}

extern "C" void positionTest(int* pos) {
  pos[0] = 2;
  pos[1] = 300;
}

//int x(const Position &p) { return p.first; }
//int y(const Position &p) { return p.second; }

inline std::pair<int, int> Pos(int x, int y) { return std::make_pair(x, y); }

inline std::ostream& operator<<(std::ostream& os, const Position& p) {
    return os << '(' << p.first << ", " << p.second << ')';
}

inline Position operator+(const Position& lhs, const Position& rhs) {
    return std::make_pair(lhs.first + rhs.first, lhs.second + rhs.second);
}

inline Position operator*(const Position& lhs, int rhs) {
    return std::make_pair(lhs.first * rhs, lhs.second * rhs);
}

inline Position operator*(int lhs, const Position& rhs) {
    return std::make_pair(rhs.first * lhs, rhs.second * lhs);
}

inline Position cut(const Position& p, const unsigned int& scale) {
    return std::make_pair(floor(p.first / scale), floor(p.second / scale));
}

inline int x(const Position& p) { return p.first; }
inline int y(const Position& p) { return p.second; }
inline void xi(Position& p) { ++p.first; }
inline void yi(Position& p) { ++p.second; }
inline void xd(Position& p) { --p.first; }
inline void yd(Position& p) { --p.second; }

/*
// An immutable position containing an (x, y) pair
class Position {
public:
    Position() {}
    Position(int x, int y) { _pos[0] = x; _pos[1] = y; }
    int x() const { return this->_pos[0]; }
    int y() const { return this->_pos[1]; }

    void operator=(const Position& rhs) { this->_pos[0] = rhs._pos[0]; this->_pos[1] = rhs._pos[1]; }
    bool operator==(const Position& rhs) const { return this->x() == rhs.x() && this->y() == rhs.y(); }
    bool operator<(const Position& rhs) const { return (this->x() < rhs.x()) || (this->x() > rhs.x() && this->y() < rhs.y()); }

    Position operator+(const Position& rhs) const {
        Position pos(this->x() + rhs.x(), this->y() + rhs.y());
        return pos;
    }
private:
    int _pos[2];
};



class InternalPosition {
public:
    InternalPosition(float x, float y) { _pos[0] = x; _pos[1] = y; }
    float x() const { return this->_pos[0]; }
    float y() const { return this->_pos[1]; }
    Position toPos() { return Position((int)_pos[0], (int)_pos[1]); }

    void operator=(const InternalPosition& rhs) { this->_pos[0] = rhs._pos[0]; this->_pos[1] = rhs._pos[1]; }
    InternalPosition operator+(const InternalPosition& rhs) const {
        InternalPosition pos(this->x() + rhs.x(), this->y() + rhs.y());
        return pos;
    }

private:
    float _pos[2];
};
*/
#endif
