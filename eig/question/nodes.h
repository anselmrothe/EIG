#pragma once
#include <vector>
#include <string>
#include <iostream>

const int ORIENTATION_VERTICAL = 0;
const int ORIENTATION_HORIZONTAL = 1;

// TODO: move this class outside this package
struct Ship {
    int label;
    int size;
    int orientation;
    int x, y;
};

class Hypothesis {
public:
    int h, w, ship_cnt;
    int *board;
    Ship *ships;
    
    Hypothesis(): h(0), w(0), ship_cnt(0), board(nullptr), ships(nullptr) {}

    Hypothesis(int _h, int _w, int* _board, int _ship_cnt, Ship* _ships): h(_h), w(_w), ship_cnt(_ship_cnt) {
        board = new int[h * w];
        ships = _ships;
        for (int i = 0; i < h * w; ++ i)
            board[i] = _board[i];
    }
    ~Hypothesis() {
        if (board != nullptr) {
            delete [] board;
        }
        if (ships != nullptr) {
            delete [] ships;
        }
    }
};


#define CREATE_FUNC_NODE(cls_name) \
class cls_name final : public FuncNode { \
public: \
    ~cls_name() { \
        for (auto node_ptr: this -> params) \
            delete node_ptr; \
    } \
    virtual void evaluate(Hypothesis*, int=-1); \
}

union value_t {
    int i;
    bool b;
    int p[2];   // for locations
};

class Node {
protected:
    std::vector<Node*> params;
    value_t _val;
public:
    virtual ~Node() = default;
    value_t val() { return this -> _val; }
    virtual void evaluate(Hypothesis*, int=-1) = 0;
};

// ====================================
// Function nodes start here
// ====================================

class FuncNode : public Node {
public:
    virtual ~FuncNode() = default;
    void add_param(Node* param) { params.push_back(param); }
    virtual void evaluate(Hypothesis*, int=-1) = 0;
};

CREATE_FUNC_NODE(EqualNode);
CREATE_FUNC_NODE(GreaterNode);
CREATE_FUNC_NODE(LessNode);
CREATE_FUNC_NODE(PlusNode);
CREATE_FUNC_NODE(MinusNode);
CREATE_FUNC_NODE(AndNode);
CREATE_FUNC_NODE(OrNode);
CREATE_FUNC_NODE(NotNode);

CREATE_FUNC_NODE(ColorFuncNode);
CREATE_FUNC_NODE(OrientFuncNode);

// ====================================
// Literal nodes start here
// ====================================

class LiteralNode : public Node {
public:
    void evaluate(Hypothesis*, int=-1) {}
};

class IntNode final : public LiteralNode {
public:
    void set_val(int i) { this -> _val.i = i; }
};

class BoolNode final : public LiteralNode {
public:
    void set_val(bool b) { this -> _val.b = b; }
};

class LocationNode final : public LiteralNode {
public:
    void set_val(int x, int y) {
        this -> _val.p[0] = x;
        this -> _val.p[1] = y;
    }
};

// ====================================
// Helper functions
// ====================================

// instantiate Node classes according to ntype
Node* build_node(std::string node_name);

// create array of arbitrary type
// use this as a workaround since Cython does not support array new
// https://stackoverflow.com/questions/51006230/dynamically-sized-array-of-objects-in-cython
template <typename T>
T* array_new(int n) {
    return new T[n];
}

//TODO: provide a logger to print the entire tree