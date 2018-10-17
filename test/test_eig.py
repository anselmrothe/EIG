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
        # 4 valid hypothesis, 2 answers are True, 2 are False for thie question
        # entropy([0.5, 0.5]) --> 1
        self.assertAlmostEqual(eig, 1)  
        
        observation[1, 2] = 2
        context.observe(observation)
        eig = compute_eig(executor, context)
        # 1 valid hypothesis, answer is False
        # no IG for asking this question
        self.assertAlmostEqual(eig, 0)
        