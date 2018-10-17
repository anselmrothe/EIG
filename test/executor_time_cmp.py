executor_setup = """
from eig.question import Parser, Executor
from eig.battleship import Ship, BattleshipHypothesis
ships = [Ship(ship_label=1, topleft=(0, 0), size=3, orientation='vertical'),
                Ship(ship_label=2, topleft=(0, 1), size=2, orientation='horizontal'),
                Ship(ship_label=3, topleft=(3, 3), size=2, orientation='horizontal'),]
hypothesis = BattleshipHypothesis(grid_size=6, ships=ships)

question = Parser.parse("(any (map (lambda y (== (color y) Red)) (set 1-1 1-2 1-3 1-4 1-5 1-6 2-1 2-2 2-3 2-4 2-5 2-6 3-1 3-2 3-3 3-4 3-5 3-6 4-1 4-2 4-3 4-4 4-5 4-6 5-1 5-2 5-3 5-4 5-5 5-6 6-1 6-2 6-3 6-4 6-5 6-6)))")
executor = Executor(question)
"""

executor_step = """
executor.execute(hypothesis)
"""

python_setup = """
from eig.battleship import Ship, BattleshipHypothesis
 
ships = [Ship(ship_label=1, topleft=(0, 0), size=3, orientation='vertical'),
                Ship(ship_label=2, topleft=(0, 1), size=2, orientation='horizontal'),
                Ship(ship_label=3, topleft=(3, 3), size=2, orientation='horizontal'),]
hypothesis = BattleshipHypothesis(grid_size=6, ships=ships)

def prog(h):
    def ly(loc):
        color_res = h.board[loc]
        eq_res = (color_res == 2)
        return eq_res
    
    set_res = {(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), 
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
        (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
        (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5),
        (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5)}
    map_res = set()
    for elem in set_res:
        map_res.add(ly(elem))
    
    any_res = False
    for elem in map_res:
        if elem is True:
            any_res = True
            break

    return any_res
"""
python_step = """
prog(hypothesis)
"""

if __name__ == "__main__":
    import timeit
    import sys
    sys.path.insert(1, sys.path[0] + "/../")

    print("=" * 50)
    print("Time for python version (100k iters):")
    time_py = timeit.repeat(stmt=python_step, setup=python_setup, repeat=5, number=100000)
    print("Min: {:3f}s, Max: {:3f}s, Avg: {:3f}s".format(min(time_py), max(time_py), sum(time_py) / 5))

    print("=" * 50)
    print("Time for C++ version (100k iters):")
    time_cpp = timeit.repeat(stmt=executor_step, setup=executor_setup, repeat=5, number=100000)
    print("Min: {:3f}s, Max: {:3f}s, Avg: {:3f}s".format(min(time_cpp), max(time_cpp), sum(time_cpp) / 5))
