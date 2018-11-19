#include "hypothesis.h"
#include <vector>
#include <algorithm>

#define pos(x, y, gs) (x) * (gs) + (y)

// Calculate partial permutation. 
// adapted from https://stackoverflow.com/questions/34866921/partial-permutations
// Requires: sequence from begin to end is sorted
//           middle is between begin and end
template<typename Bidi, typename Functor>
void for_each_permuted_combination(Bidi begin,
                                   Bidi middle,
                                   Bidi end,
                                   Functor func) {
    do {
        func(begin, middle);
        std::reverse(middle, end);
    } while (std::next_permutation(begin, end));
}

int* create_board(int grid_size, int ship_cnt, Ship* ships) {
    int* board = new int[grid_size * grid_size]();
    for (int i = 0; i < ship_cnt; ++ i) {
        int step_x, step_y, label = ships[i].label;
        if (ships[i].orientation == ORIENTATION_HORIZONTAL)
            step_x = 0, step_y = 1;
        else step_x = 1, step_y = 0;
        int pos_x = ships[i].x, pos_y = ships[i].y;
        if (board[pos(pos_x, pos_y, grid_size)] != 0) goto fault;
        board[pos(pos_x, pos_y, grid_size)] = label;
        for (int j = 1; j < ships[i].size; ++ j) {
            pos_x += step_x;
            pos_y += step_y;
            if (pos_x >= grid_size || pos_y >= grid_size || 
                board[pos(pos_x, pos_y, grid_size)] != 0) goto fault;
            board[pos(pos_x, pos_y, grid_size)] = label;
        }
    }
    return board;

fault:
    delete[] board;
    return nullptr;
}

void create_hypothesis_space(int grid_size, std::vector<int>& labels, std::vector<int>& sizes, 
        std::vector<int>& orientations, std::vector<Hypothesis*>& hypotheses) {

    // calculate all possible topleft positions
    std::vector<int> toplefts;
    for (int i = 0; i < grid_size; ++ i)
        for (int j = 0; j < grid_size; ++ j)
            toplefts.push_back(pos(i, j, grid_size));
    
    // encode each ship configuration as an integer
    // since ships with different colors are symmetric, we only need to enumerate configs for one ship
    // use maximum number of all parameters as value index
    int index = std::max(toplefts.size(), std::max(sizes.size(), orientations.size()));
    std::vector<int> ship_space;
    for (int size: sizes)
        for (int orient: orientations)
            for (int topleft: toplefts)
                ship_space.push_back(((size * index) + orient) * index + topleft);
    std::sort(ship_space.begin(), ship_space.end());

    // calculate permutations for all ships
    // code adapted from https://stackoverflow.com/questions/34866921/partial-permutations
    for_each_permuted_combination(ship_space.begin(), ship_space.begin() + labels.size(), ship_space.end(),
        [&](std::vector<int>::iterator first, std::vector<int>::iterator last)
        {
            Ship *ships = new Ship[labels.size()];
            for (size_t i = 0; first != last; ++first, ++i) {
                int config = *first;
                // decode configuration
                int topleft = config % index;
                ships[i].orientation = (config / index) % index;
                ships[i].size = (config / index) / index;
                ships[i].x = topleft / grid_size;
                ships[i].y = topleft % grid_size;
                ships[i].label = labels[i];
            }
            int* board = create_board(grid_size, labels.size(), ships);
            if (board == nullptr) return false;
            else {
                /*std::cout << ships[0].size << " " << ships[0].x << " " << ships[0].y << std::endl;
                std::cout << ships[1].size << " " << ships[1].x << " " << ships[1].y << std::endl;
                std::cout << std::endl;*/
                hypotheses.push_back(new Hypothesis(grid_size, grid_size, board, labels.size(), ships));
                // TODO: directly use this array when instantiating new Hypothesis.
                delete[] board;
            }
        });
}

bool match(int size, int* h, int* b) {
    for (int i = 0; i < size; ++ i) {
        if (b[i] == -1) continue;
        if (b[i] != h[i]) return false;
    }
    return true;
}

void match_hypotheses_observation(int* board, std::vector<Hypothesis*>& hypotheses, std::vector<int>& valid_ids) {

    int size = hypotheses[0] -> h * hypotheses[0] -> w;
    for (size_t i = 0; i < hypotheses.size(); ++ i) {
        if (match(size, hypotheses[i] -> board, board))
            valid_ids.push_back(i);
    }
}