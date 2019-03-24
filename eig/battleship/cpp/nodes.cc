#include "nodes.h"

#define evaluate_child(child_num) \
    for (int _i = 0; _i < (child_num); ++ _i) \
        this -> _params[_i] -> evaluate(h, lambda_args)

void EqualNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(2);
    this -> _val.b = (this -> _params[0] -> val().i == this -> _params[1] -> val().i);
}

void SetEqualNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(1);
    this -> _val.b = true;
    int first_v = *(((SetFuncNode*)this -> _params[0]) -> set.begin());
    for (auto i: ((SetFuncNode*)this -> _params[0]) -> set) {
        if (i != first_v) {
            this -> _val.b = false;
            break;
        }
    }
}

void GreaterNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(2);
    this -> _val.b = (this -> _params[0] -> val().i > this -> _params[1] -> val().i);
}

void LessNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(2);
    this -> _val.b = (this -> _params[0] -> val().i < this -> _params[1] -> val().i);
}

void PlusNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(2);
    this -> _val.i = this -> _params[0] -> val().i + this -> _params[1] -> val().i;
}

void MinusNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(2);
    this -> _val.i = this -> _params[0] -> val().i - this -> _params[1] -> val().i;
}

void SumNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(1);
    this -> _val.i = 0;
    for (auto i: ((SetFuncNode*)this -> _params[0]) -> set) {
        this -> _val.i += i;
    }
}

void AndNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(2);
    this -> _val.b = this -> _params[0] -> val().b && this -> _params[1] -> val().b;
}

void OrNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(2);
    this -> _val.b = this -> _params[0] -> val().b || this -> _params[1] -> val().b;
}

void NotNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(1);
    this -> _val.b = !(this -> _params[0] -> val().b);
}

void RowNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(1);
    this -> _val.i = int(this -> _params[0] -> val().p[0]) + 1;
}

void ColNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(1);
    this -> _val.i = int(this -> _params[0] -> val().p[1]) + 1;
}

void AnyNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(1);
    this -> _val.b = false;
    for (auto i: ((SetFuncNode*)this -> _params[0]) -> set) {
        if (i == 1) {
            this -> _val.b = true;
            break;
        }
    }
}

void AllNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(1);
    this -> _val.b = true;
    for (auto i: ((SetFuncNode*)this -> _params[0]) -> set) {
        if (i == 0) {
            this -> _val.b = false;
            break;
        }
    }
}

void TopLeftNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(1);
    short x = h -> h, y = h -> w;
    for (auto i: ((SetFuncNode*)this -> _params[0]) -> set) {
        value_t pos = {i};
        if (pos.p[0] < x || (pos.p[0] == x && pos.p[1] < y))
            x = pos.p[0], y = pos.p[1];
    }
    this -> _val.p[0] = x;
    this -> _val.p[1] = y;
}

void BottomRightNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(1);
    short x = 0, y = 0;
    for (auto i: ((SetFuncNode*)this -> _params[0]) -> set) {
        value_t pos = {i};
        if (pos.p[0] > x || (pos.p[0] == x && pos.p[1] > y))
            x = pos.p[0], y = pos.p[1];
    }
    this -> _val.p[0] = x;
    this -> _val.p[1] = y;
}

void SetSizeNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(1);
    this -> _val.i = ((SetFuncNode*)this -> _params[0]) -> set.size();
}

void IsSubsetNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(2);
    SetFuncNode* set1 = (SetFuncNode*)this -> _params[0];
    SetFuncNode* set2 = (SetFuncNode*)this -> _params[1];
    this -> _val.b = true;
    for (auto i: set1 -> set) {
        if (set2 -> set.find(i) == set2 -> set.end()) {
            this -> _val.b = false;
            break;
        }
    }
}

void ColorFuncNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(1);
    value_t loc = this -> _params[0] -> val();
    int x = loc.p[0], y = loc.p[1];
    this -> _val.i = h -> board[x * h -> w + y];
}

void OrientFuncNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(1);
    int ship_label = this -> _params[0] -> val().i;
    bool flag = false;
    for (int i = 0; i < h -> ship_cnt; ++ i) {
        if (h -> ships[i].label == ship_label) {
            this -> _val.i = h -> ships[i].orientation;
            flag = true;
            break;
        }
    }
    // invoke runtime error if ship_label is not in h -> ships
    if (!flag) throw RuntimeException("Ship not found!");
}

// binary trick here
// ORIENTATION_VERTICAL + 1 = 1 => (01)_2
// ORIENTATION_HORIZONTAL + 1 = 2 => (10)_2
#define step_x(orientation) ((orientation + 1) & 1)
#define step_y(orientation) (((orientation + 1) & 2) >> 1)

void TouchFuncNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(2);
    int ship_label_1 = this -> _params[0] -> val().i;
    int ship_label_2 = this -> _params[1] -> val().i;
    int step_x1, step_x2, step_y1, step_y2;
    int size1 = 0, size2 = 0, x1, y1, x2, y2, x2_init, y2_init;
    // find the properties of both ships
    for (int i = 0; i < h -> ship_cnt; ++ i) {
        if (h -> ships[i].label == ship_label_1) {
            int orientation = h -> ships[i].orientation;
            step_x1 = step_x(orientation);
            step_y1 = step_y(orientation);
            x1 = h -> ships[i].x; y1 = h -> ships[i].y;
            size1 = h -> ships[i].size;
        }
        if (h -> ships[i].label == ship_label_2) {
            int orientation = h -> ships[i].orientation;
            step_x2 = step_x(orientation);
            step_y2 = step_y(orientation);
            x2_init = h -> ships[i].x; y2_init = h -> ships[i].y;
            size2 = h -> ships[i].size;
        }
    }
    // invoke runtime error if ship_label is not in h -> ships
    if (size1 == 0 || size2 == 0) throw RuntimeException("Ship not found!");
    this -> _val.b = false;
    // for each pair of locations, see if they touch
    for (int i = 0; i < size1; ++ i) {
        x2 = x2_init; y2 = y2_init;
        for (int j = 0; j < size2; ++ j) {
            int diff = 0;
            if (x1 > x2) diff += (x1 - x2);
            else diff += (x2 - x1);
            if (y1 > y2) diff += (y1 - y2);
            else diff += (y2 - y1);
            if (diff == 1) {
                this -> _val.b = true;
                return;
            }
            x2 += step_x2; y2 += step_y2;
        }
        x1 += step_x1; y1 += step_y1;
    }
}

void SizeFuncNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(1);
    int ship_label = this -> _params[0] -> val().i;
    bool flag = false;
    for (int i = 0; i < h -> ship_cnt; ++ i) {
        if (h -> ships[i].label == ship_label) {
            this -> _val.i = h -> ships[i].size;
            flag = true;
            break;
        }
    }
    // invoke runtime error if ship_label is not in h -> ships
    if (!flag) throw RuntimeException("Ship not found!");
}

void ColoredTilesFuncNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(1);
    this -> set.clear();
    int ship_label = this -> _params[0] -> val().i;
    bool flag = false;
    for (int i = 0; i < (h -> w * h -> h); ++ i)
        if (h -> board[i] == ship_label) {
            value_t pos;
            pos.p[0] = i / (h -> w);
            pos.p[1] = i % (h -> w);
            this -> set.insert(pos.i);
            flag = true;
        }
    // invoke runtime error if ship_label is not in h -> ships
    if (!flag) throw RuntimeException("Ship not found!");
}

void MapNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    this -> set.clear();
    this -> _params[1] -> evaluate(h, lambda_args);
    // The lambda variable name is two levels down
    // i.e. map_op -> lambda_op -> lambda_var
    std::string name = this -> _params[0] -> params(0) -> name();
    for (auto i: ((SetFuncNode*)this -> _params[1]) -> set) {
        lambda_args[name] = i;
        this -> _params[0] -> evaluate(h, lambda_args);
        this -> set.insert(this -> _params[0] -> val().i);
    }
    lambda_args.erase(name);
}

void SetNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    this -> set.clear();
    for (auto node_ptr: this -> _params) {
        node_ptr -> evaluate(h, lambda_args);
        int childv = node_ptr -> val().i;
        if (childv == SET_COLORS) {
            for (int i = 0; i < h -> ship_cnt; ++ i)
                this -> set.insert((h -> ships[i]).label);
            break;
        } else if (childv == SET_LOCATIONS) {
            for (int i = 0; i < h -> h; ++ i)
                for (int j = 0; j < h -> w; ++ j) {
                    value_t pos;
                    pos.p[0] = i, pos.p[1] = j;
                    this -> set.insert(pos.i);
                }
            break;
        }
        if (this -> set.find(childv) == this -> set.end())
            this -> set.insert(childv);
    }
}

void SetDiffNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(2);
    auto& param_set1 = ((SetFuncNode*)this -> _params[0]) -> set;
    auto& param_set2 = ((SetFuncNode*)this -> _params[1]) -> set;
    this -> set.clear();
    std::unordered_set<int> temp_set;
    for (auto i: param_set1) {
        if (param_set2.find(i) == param_set2.end())
            temp_set.insert(i);
    }
    this -> set.insert(temp_set.begin(), temp_set.end());
}

void UnionNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(2);
    this -> set.clear();
    std::unordered_set<int> temp_set;
    for (auto i: ((SetFuncNode*)this -> _params[0]) -> set)
        temp_set.insert(i);
    for (auto i: ((SetFuncNode*)this -> _params[1]) -> set)
        temp_set.insert(i);
    this -> set.insert(temp_set.begin(), temp_set.end());
}

void IntersectNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(2);
    auto& param_set1 = ((SetFuncNode*)this -> _params[0]) -> set;
    auto& param_set2 = ((SetFuncNode*)this -> _params[1]) -> set;
    this -> set.clear();
    std::unordered_set<int> temp_set;
    for (auto i: param_set1) {
        if (param_set2.find(i) != param_set2.end())
            temp_set.insert(i);
    }
    this -> set.insert(temp_set.begin(), temp_set.end());
}

void UniqueNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    evaluate_child(1);
    this -> set.clear();
    auto& param_set = ((SetFuncNode*)this -> _params[0]) -> set;
    std::unordered_set<int> temp_set(param_set.begin(), param_set.end());
    this -> set.insert(temp_set.begin(), temp_set.end());
}

void LambdaNode::evaluate(Hypothesis* h, std::unordered_map<std::string, int>& lambda_args) {
    this -> _params[1] -> evaluate(h, lambda_args);
    this -> _val.i = this -> _params[1] -> val().i;
}

Node* build_node(std::string node_name) {
    if (node_name == "equal") return new EqualNode();
    else if (node_name == "set_equal") return new SetEqualNode();
    else if (node_name == "greater") return new GreaterNode();
    else if (node_name == "less") return new LessNode();
    else if (node_name == "plus") return new PlusNode();
    else if (node_name == "minus") return new MinusNode();
    else if (node_name == "sum_op") return new SumNode();
    else if (node_name == "and_op") return new AndNode();
    else if (node_name == "or_op") return new OrNode();
    else if (node_name == "not_op") return new NotNode();
    else if (node_name == "row") return new RowNode();
    else if (node_name == "col") return new ColNode();
    else if (node_name == "topleft") return new TopLeftNode();
    else if (node_name == "bottomright") return new BottomRightNode();
    else if (node_name == "set_size") return new SetSizeNode();
    else if (node_name == "is_subset") return new IsSubsetNode();

    else if (node_name == "color_fn") return new ColorFuncNode();
    else if (node_name == "orient_fn") return new OrientFuncNode();
    else if (node_name == "touch_fn") return new TouchFuncNode();
    else if (node_name == "size_fn") return new SizeFuncNode();
    else if (node_name == "colored_tiles_fn") return new ColoredTilesFuncNode();


    else if (node_name == "any_op") return new AnyNode();
    else if (node_name == "all_op") return new AllNode();
    else if (node_name == "map_op") return new MapNode();
    else if (node_name == "set_op") return new SetNode();
    else if (node_name == "set_diff") return new SetDiffNode();
    else if (node_name == "union") return new UnionNode();
    else if (node_name == "intersect") return new IntersectNode();
    else if (node_name == "unique") return new UniqueNode();
    else if (node_name == "lambda_op") return new LambdaNode();

    else if (node_name == "number") return new IntNode();
    else if (node_name == "boolean") return new BoolNode();
    else if (node_name == "color") return new IntNode();
    else if (node_name == "location") return new LocationNode();
    else if (node_name == "orientation") return new IntNode();
    else if (node_name == "set_color") return new IntNode();
    else if (node_name == "set_location") return new IntNode();
    else if (node_name == "lambda_x" or node_name == "lambda_y") return new LambdaVarNode();
    // TODO: invoke runtime error if reach here
}