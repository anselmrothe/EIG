#include "nodes.h"

void EqualNode::evaluate(Hypothesis* h, int lambda_var) {
    this -> params[0] -> evaluate(h, lambda_var);
    this -> params[1] -> evaluate(h, lambda_var);
    this -> _val.b = (this -> params[0] -> val().i == this -> params[1] -> val().i);
}

void GreaterNode::evaluate(Hypothesis* h, int lambda_var) {
    this -> params[0] -> evaluate(h, lambda_var);
    this -> params[1] -> evaluate(h, lambda_var);
    this -> _val.b = (this -> params[0] -> val().i > this -> params[1] -> val().i);
}

void LessNode::evaluate(Hypothesis* h, int lambda_var) {
    this -> params[0] -> evaluate(h, lambda_var);
    this -> params[1] -> evaluate(h, lambda_var);
    this -> _val.b = (this -> params[0] -> val().i < this -> params[1] -> val().i);
}

void PlusNode::evaluate(Hypothesis* h, int lambda_var) {
    this -> params[0] -> evaluate(h, lambda_var);
    this -> params[1] -> evaluate(h, lambda_var);
    this -> _val.i = this -> params[0] -> val().i + this -> params[1] -> val().i;
}

void MinusNode::evaluate(Hypothesis* h, int lambda_var) {
    this -> params[0] -> evaluate(h, lambda_var);
    this -> params[1] -> evaluate(h, lambda_var);
    this -> _val.i = this -> params[0] -> val().i - this -> params[1] -> val().i;
}

void AndNode::evaluate(Hypothesis* h, int lambda_var) {
    this -> params[0] -> evaluate(h, lambda_var);
    this -> params[1] -> evaluate(h, lambda_var);
    this -> _val.b = this -> params[0] -> val().b && this -> params[1] -> val().b;
}

void OrNode::evaluate(Hypothesis* h, int lambda_var) {
    this -> params[0] -> evaluate(h, lambda_var);
    this -> params[1] -> evaluate(h, lambda_var);
    this -> _val.b = this -> params[0] -> val().b || this -> params[1] -> val().b;
}

void NotNode::evaluate(Hypothesis* h, int lambda_var) {
    this -> params[0] -> evaluate(h, lambda_var);
    this -> _val.b = !(this -> params[0] -> val().b);
}

void ColorFuncNode::evaluate(Hypothesis* h, int lambda_var) {
    this -> params[0] -> evaluate(h, lambda_var);
    value_t loc = this -> params[0] -> val();
    int x = loc.p[0], y = loc.p[1];
    this -> _val.i = h -> board[x * h -> w + y];
}

void OrientFuncNode::evaluate(Hypothesis* h, int lambda_var) {
    this -> params[0] -> evaluate(h, lambda_var);
    int ship_label = this -> params[0] -> val().i;
    for (int i = 0; i < h -> ship_cnt; ++ i) {
        if (h -> ships[i].label == ship_label) {
            this -> _val.i = h -> ships[i].orientation;
            break;
        }
    }
    // TODO: Invoke runtime error if ship_label is not in h -> ships
}

void AnyNode::evaluate(Hypothesis* h, int lambda_var) {
    this -> params[0] -> evaluate(h, lambda_var);
    this -> _val.b = false;
    for (auto i: ((SetFuncNode*)this -> params[0]) -> set) {
        if (i == 1) {
            this -> _val.b = true;
            break;
        }
    }
}

void MapNode::evaluate(Hypothesis* h, int lambda_var) {
    this -> set.clear();
    this -> params[1] -> evaluate(h);
    for (auto i: ((SetFuncNode*)this -> params[1]) -> set) {
        this -> params[0] -> evaluate(h, i);
        this -> set.insert(this -> params[0] -> val().i);
    }
}

void SetNode::evaluate(Hypothesis* h, int lambda_var) {
    this -> set.clear();
    for (auto node_ptr: params) {
        node_ptr -> evaluate(h);
        this -> set.insert(node_ptr -> val().i);
    }
}

void LambdaNode::evaluate(Hypothesis* h, int lambda_var) {
    this -> params[1] -> evaluate(h, lambda_var);
    this -> _val.i = this -> params[1] -> val().i;
}

Node* build_node(std::string node_name) {
    if (node_name == "equal") return new EqualNode();
    else if (node_name == "greater") return new GreaterNode();
    else if (node_name == "less") return new LessNode();
    else if (node_name == "plus") return new PlusNode();
    else if (node_name == "minus") return new MinusNode();
    else if (node_name == "and") return new AndNode();
    else if (node_name == "or") return new OrNode();
    else if (node_name == "not") return new NotNode();

    else if (node_name == "color_fn") return new ColorFuncNode();
    else if (node_name == "orient_fn") return new OrientFuncNode();

    else if (node_name == "any") return new AnyNode();
    else if (node_name == "map") return new MapNode();
    else if (node_name == "set") return new SetNode();
    else if (node_name == "lambda") return new LambdaNode();

    else if (node_name == "number") return new IntNode();
    else if (node_name == "boolean") return new BoolNode();
    else if (node_name == "color") return new IntNode();
    else if (node_name == "location") return new LocationNode();
    else if (node_name == "orientation") return new IntNode();
    else if (node_name == "lambda_x" or node_name == "lambda_y") return new LambdaVarNode();
    // TODO: invoke runtime error if reach here
}