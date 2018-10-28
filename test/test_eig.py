from eig import compute_eig, Bayes, Context
from eig.battleship import BattleshipHypothesesSpace, Parser, Executor
import unittest
import numpy as np
from math import log2


class TestEIG(unittest.TestCase):

    def test_eig(self):
        hs = BattleshipHypothesesSpace(grid_size=3, ship_labels=[1, 2], 
                ship_sizes=[2, 3], orientations=['V', 'H'])
        belief = Bayes(len(hs))
        observation = np.zeros((3, 3)) - 1
        observation[0, 0] = 0
        observation[1, 0] = observation[2, 0] = 1
        observation[1, 1] = 2
        
        context = Context(hs, belief)
        context.observe(observation)
        
        question = Parser.parse("Red")
        executor = Executor(question)
        eig = compute_eig(executor, context)
        # no IG for asking this question
        self.assertAlmostEqual(eig, 0)
        
        question = Parser.parse("(any (map (lambda y (== (color y) Red)) (set 1-1 1-2 1-3)))")
        executor = Executor(question)
        eig = compute_eig(executor, context)
        # 4 valid hypothesis, 2 answers are True, 2 are False for this question
        # entropy([0.5, 0.5]) = 1
        self.assertAlmostEqual(eig, 1)

        question = Parser.parse("(size Red)")
        executor = Executor(question)
        eig = compute_eig(executor, context)
        # 4 valid hypothesis, 1 answers is 3, 3 are 2 for this question
        # entropy([0.25, 0.75]) = 2 - 0.75*log(3)
        self.assertAlmostEqual(eig, 2 - 0.75 * log2(3))
        
        observation[1, 2] = 2
        context.observe(observation)
        eig = compute_eig(executor, context)
        # 1 valid hypothesis, answer is False
        # no IG for asking this question
        self.assertAlmostEqual(eig, 0)
        