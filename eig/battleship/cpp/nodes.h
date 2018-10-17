#pragma once
#include <vector>
#include <string>
#include <iostream>
#include <unordered_set>
#include "hypothesis.h"


#define CREATE_FUNC_NODE(cls_name, base) \
class cls_name final : public base { \
public: \
    ~cls_name() { \
        for (auto node_ptr: this -> FuncNode::params) \
            delete node_ptr; \
    } \
    virtual void evaluate(Hypothesis*, int=-1); \
}

union value_t {
    int i;
    bool b;
    short p[2];   // for locations
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

class SetFuncNode : public FuncNode {
public:
    // Instead of providing a hashing function for union,
    // here we store all values as int, and use union type
    //  value_t to interpret it when needed.
    std::unordered_set<int> set;
};

CREATE_FUNC_NODE(EqualNode, FuncNode);
CREATE_FUNC_NODE(GreaterNode, FuncNode);
CREATE_FUNC_NODE(LessNode, FuncNode);
CREATE_FUNC_NODE(PlusNode, FuncNode);
CREATE_FUNC_NODE(MinusNode, FuncNode);
CREATE_FUNC_NODE(AndNode, FuncNode);
CREATE_FUNC_NODE(OrNode, FuncNode);
CREATE_FUNC_NODE(NotNode, FuncNode);

CREATE_FUNC_NODE(ColorFuncNode, FuncNode);
CREATE_FUNC_NODE(OrientFuncNode, FuncNode);

CREATE_FUNC_NODE(AnyNode, FuncNode);
CREATE_FUNC_NODE(MapNode, SetFuncNode);
CREATE_FUNC_NODE(SetNode, SetFuncNode);
CREATE_FUNC_NODE(LambdaNode, FuncNode);

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
    void set_val(short x, short y) {
        this -> _val.p[0] = x;
        this -> _val.p[1] = y;
    }
};

class LambdaVarNode final : public Node {
public:
    void evaluate(Hypothesis*, int lambda_var) {
        this -> _val.i = lambda_var;
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