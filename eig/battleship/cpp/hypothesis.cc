#include "hypothesis.h"
#include <unordered_map>
#include <vector>
#include <algorithm>

#define pos(x, y, gs) (x) * (gs) + (y)
using std::vector;
using std::unordered_map;

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

void create_hypothesis_space(int grid_size, vector<int>& labels, vector<int>& sizes, 
        vector<int>& orientations, vector<Hypothesis*>& hypotheses) {

    // calculate all possible topleft positions
    vector<int> toplefts;
    for (int i = 0; i < grid_size; ++ i)
        for (int j = 0; j < grid_size; ++ j)
            toplefts.push_back(pos(i, j, grid_size));
    
    // encode each ship configuration as an integer
    // since ships with different colors are symmetric, we only need to enumerate configs for one ship
    // use maximum number of all parameters as value index
    int index = std::max(toplefts.size(), std::max(sizes.size(), orientations.size()));
    vector<int> ship_space;
    for (int size: sizes)
        for (int orient: orientations)
            for (int topleft: toplefts)
                ship_space.push_back(((size * index) + orient) * index + topleft);
    std::sort(ship_space.begin(), ship_space.end());

    // calculate permutations for all ships
    // code adapted from https://stackoverflow.com/questions/34866921/partial-permutations
    for_each_permuted_combination(ship_space.begin(), ship_space.begin() + labels.size(), ship_space.end(),
        [&](vector<int>::iterator first, vector<int>::iterator last)
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

void match_hypotheses_observation(int* board, vector<Hypothesis*>& hypotheses, vector<int>& valid_ids) {

    int size = hypotheses[0] -> h * hypotheses[0] -> w;
    for (size_t i = 0; i < hypotheses.size(); ++ i) {
        if (match(size, hypotheses[i] -> board, board))
            valid_ids.push_back(i);
    }
}

void generate_combination(const unordered_map< int, vector<int> >& data, const vector<int>& labels, int step, 
        vector<int>& current_result, vector< vector<int> >& results) {
    if (step == labels.size()) {
        results.push_back(vector<int>(current_result));
        return;
    }
    int label = labels[step];
    for (int choice: data.at(label)) {
        current_result[step] = choice;
        generate_combination(data, labels, step + 1, current_result, results);
    }
}

void create_hypotheses_from_observation_c(int* board, int grid_size, vector<int>& labels, vector<int>& sizes, 
        vector<int>& orientations, vector<Hypothesis*>& hypotheses) {
    
    int board_size = grid_size * grid_size;
    // for each ship, first check the observed board for constraints
    unordered_map<int, int> observed_topleft, observed_size, orientation_mask;
    for (int label: labels) {
        // default values
        observed_topleft[label] = -1;
        orientation_mask[label] = (ORIENTATION_VERTICAL + 1) | (ORIENTATION_HORIZONTAL + 1);
        observed_size[label] = 0;
        for (int i = 0; i < board_size; i ++) {
            int x = i / grid_size;
            int y = i % grid_size;
            if (board[i] == label) {
                observed_topleft[label] = i;
                int len = 1;
                // check to the right or below
                if (y < grid_size - 1 && board[i + 1] == label) {
                    orientation_mask[label] = ORIENTATION_HORIZONTAL + 1;
                    len ++;
                    while (y + len < grid_size && board[i + len] == label) len ++;
                } else if (x < grid_size - 1 && board[i + grid_size] == label) {
                    orientation_mask[label] = ORIENTATION_VERTICAL + 1;
                    len ++;
                    while (x + len < grid_size && board[i + len * grid_size] == label) len ++;
                }
                observed_size[label] = len;
                // check orientation for length 1 tile
                if (len == 1) {
                    orientation_mask[label] = 0;
                    if ((y > 0 && board[i - 1] == -1) || (y < grid_size - 1 && board[i + 1] == -1))
                        orientation_mask[label] |= (ORIENTATION_HORIZONTAL + 1);
                    if ((x > 0 && board[i - grid_size] == -1) || (x < grid_size - 1 && board[i + grid_size] == -1))
                        orientation_mask[label] |= (ORIENTATION_VERTICAL + 1);
                }
                break;
            }
        }
        
        //std::cout << "Ship: " << label << " topleft " << observed_topleft[label] << " size " << observed_size[label] << " orient " << orientation_mask[label] << std::endl;
    }

    // for each ship, get different configurations encoded as an integer
    unordered_map< int, vector<int> > ship_configs;
    int index = std::max(size_t(board_size), std::max(sizes.size(), orientations.size()));
    for (int label: labels) {
        for (int orient: orientations) {
            if (!((orient + 1) & orientation_mask[label])) continue;
            int offset = orient == ORIENTATION_HORIZONTAL ? -1 : -grid_size;
            int topleft = observed_topleft[label];
            int size_base = observed_size[label];
            if (topleft != -1) {
                // try to move towards top or left
                while (topleft >= 0) {
                    for (int size: sizes) {
                        if (size < size_base) continue;
                        ship_configs[label].push_back(((size * index) + orient) * index + topleft);
                        if (topleft - size * offset >= board_size || board[topleft - size * offset] != -1) break;
                    }
                    size_base ++;
                    topleft += offset;
                    if (board[topleft] != -1) break;
                }
            } else {
                // try every empty slot
                for (int topleft = 0; topleft < board_size; topleft ++) {
                    if (board[topleft] == -1) {
                        for (int size: sizes) {
                            ship_configs[label].push_back(((size * index) + orient) * index + topleft);
                            if (topleft - size * offset >= board_size || board[topleft - size * offset] != -1) break;
                        }
                    }
                }
            }
        }
        if (ship_configs[label].size() == 0) {
            // the board is invalid, just return
            return;
        }
    }

    // create hypotheses
    vector< vector<int> > config_combinations;
    vector<int> tmp(labels.size());
    generate_combination(ship_configs, labels, 0, tmp, config_combinations);
    for (auto& configs: config_combinations) {
        Ship *ships = new Ship[labels.size()];
        for (size_t i = 0; i < labels.size(); i ++) {
            // decode configuration
            int config = configs[i];
            int topleft = config % index;
            ships[i].orientation = (config / index) % index;
            ships[i].size = (config / index) / index;
            ships[i].x = topleft / grid_size;
            ships[i].y = topleft % grid_size;
            ships[i].label = labels[i];
        }
        int* new_board = create_board(grid_size, labels.size(), ships);
        if (new_board == nullptr) continue;
        if (match(board_size, new_board, board)) {
            hypotheses.push_back(new Hypothesis(grid_size, grid_size, new_board, labels.size(), ships));
            delete[] new_board;
        }
    }
}
