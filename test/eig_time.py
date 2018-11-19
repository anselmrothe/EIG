import sys
sys.path.insert(1, sys.path[0] + "/../")

import eig
from eig.battleship import BattleshipHypothesisSpace, Parser, Executor, EqualSizesDistribution
import numpy as np
import time

PROG = "(any (map (lambda y (== (color y) Red)) (set 1-1 1-2 1-3 1-4 1-5 1-6 2-1 2-2 2-3 2-4 2-5 2-6 3-1 3-2 3-3 3-4 3-5 3-6 4-1 4-2 4-3 4-4 4-5 4-6 5-1 5-2 5-3 5-4 5-5 5-6 6-1 6-2 6-3 6-4 6-5 6-6)))"
OBS = np.array([[-1, 1, 1, 1, -1, 2],
 [-1, 0, -1, 0, 0, 3],
 [-1, 0, -1, -1, 3, -1],
 [0, -1, -1, 0, 3, -1],
 [-1, -1, 0, 0, 0, 0],
 [-1, 0, 0, -1, -1, 0]])

def run_build_space():
    return BattleshipHypothesisSpace(grid_size=6, ship_labels=[1, 2, 3], 
        ship_sizes=[2, 3, 4], orientations=['V', 'H'])


def run_update_context(hs):
    prior = EqualSizesDistribution(ship_labels=[1, 2, 3])
    belief = eig.Bayes(hs, prior)
    context = eig.Context(hs, belief)
    context.observe(OBS)
    return context


def run_calculate(context):
    question = Parser.parse(PROG)
    executor = Executor(question)
    eig_s = eig.compute_eig(executor, context)
    return eig_s


def run_multiple(hs, time=100):
    for _ in range(time):
        belief = eig.Bayes(hs)
        context = eig.Context(hs, belief)
        context.observe(OBS)
        question = Parser.parse(PROG)
        executor = Executor(question)
        eig_s = eig.compute_eig(executor, context)


if __name__ == "__main__":
    # test run single time
    time0 = time.time()
    hs = run_build_space()
    time1 = time.time()
    ctx = run_update_context(hs)
    time2 = time.time()
    eig_s = run_calculate(ctx)
    time3 = time.time()

    t_create_space = time1 - time0
    t_update_belief = time2 - time1
    t_calc_eig = time3 - time2
    t_total = time3 - time0
    print("Total time: {:.3f}".format(t_total))
    print("Time for creating hypothesis space: {:.3f}".format(t_create_space))
    print("Time for updating belief: {:.3f}".format(t_update_belief))
    print("Time for calculating EIG: {:.3f}".format(t_calc_eig))

    # test run multiple time
    time0 = time.time()
    run_multiple(hs)
    time1 = time.time()
    print("Time for calculating EIG {} times: {:.3f}".format(100, time1 - time0))