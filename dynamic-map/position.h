// An immutable position containing an (x, y) pair
class Position {
public:
    Position(float x, float y) : _x(x), _y(y) {}
    float x() { return this->_x; }
    float y() { return this->_y; }
private:
    float _x;
    float _y;
};
