import sys
sys.path.insert(1, sys.path[0] + "/../")

from eig.eig import compute_eig
from eig.bayes import Bayes
from eig.context import Context
from eig.battleship.hypothesis import BattleshipHypothesesSpace
from eig.battleship.question import Parser, Executor
import numpy as np
import time


if __name__ == "__main__":
    time0 = time.time()
    hs = BattleshipHypothesesSpace(grid_size=6, ship_labels=[1, 2, 3], 
    ship_sizes=[2, 3, 4], orientations=['vertical', 'horizontal'])

    time1 = time.time()
    belief = Bayes(len(hs))
    observation = np.zeros((6, 6)) - 1
    observation[2, 1] = observation[2, 3] = observation[3, 3] = observation[3, 4] = 0
    observation[3, 1] = 1
    observation[3, 2] = 2

    context = Context(hs, belief)
    context.observe(observation)

    time2 = time.time()
    question = Parser.parse("(any (map (lambda y (== (color y) Red)) (set 1-1 1-2 1-3)))")
    executor = Executor(question)
    eig = compute_eig(executor, context)

    time3 = time.time()

    t_create_space = time1 - time0
    t_update_belief = time2 - time1
    t_calc_eig = time3 - time2
    t_total = time3 - time0
    print("Total time: {:.3f}".format(t_total))
    print("Time for creating hypothesis space: {:.3f}".format(t_create_space))
    print("Time for updating belief: {:.3f}".format(t_update_belief))
    print("Time for calculating EIG: {:.3f}".format(t_calc_eig))