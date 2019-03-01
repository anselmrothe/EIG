#pragma once
#include <iostream>
#include <vector>

const int ORIENTATION_VERTICAL = 0;
const int ORIENTATION_HORIZONTAL = 1;
const int SET_COLORS = -1;
const int SET_LOCATIONS = -2;

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

int* create_board(int grid_size, int ship_cnt, Ship* ships);

void create_hypothesis_space(int, std::vector<int>&, std::vector<int>&, std::vector<int>&, std::vector<Hypothesis*>&);

void match_hypotheses_observation(int*, std::vector<Hypothesis*>&, std::vector<int>&);