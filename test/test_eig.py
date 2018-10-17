from eig.eig import compute_eig
from eig.bayes import Bayes
from eig.context import Context
from eig.battleship.hypothesis import BattleshipHypothesesSpace
from eig.battleship.question import Parser, Executor
import unittest
import numpy as np

class TestEIG(unittest.TestCase):

    def test_eig(self):
        hs = BattleshipHypothesesSpace(grid_size=3, ship_labels=[1, 2], 
                ship_sizes=[2, 3], orientations=['vertical', 'horizontal'])
        belief = Bayes(len(hs))
        context = Context(hs, belief)
        context.observe(np.array([-1, -1, -1, 2, -1, -1, -1, 0, -1]).reshape((3, 3)))

        question = Parser.parse("(any (map (lambda y (== (color y) Red)) (set 1-1 1-2 1-3)))")
        executor = Executor(question)
        eig = compute_eig(executor, context)
        print(eig)

        question = Parser.parse("Red")
        executor = Executor(question)
        eig = compute_eig(executor, context)
        print(eig)
        