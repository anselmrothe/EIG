from eig import compute_eig, compute_eig_basic, Bayes, Context
from eig.battleship import BattleshipHypothesisSpace, Parser, Executor, EqualSizesDistribution
import unittest
import numpy as np

class TestEIG(unittest.TestCase):

    def setUp(self):
        self.hs1 = BattleshipHypothesisSpace(grid_size=3, ship_labels=[1, 2], 
                ship_sizes=[2, 3], orientations=['V', 'H'])
        
        self.observation1 = np.zeros((3, 3)) - 1
        self.observation1[0, 0] = 0
        self.observation1[1, 0] = self.observation1[2, 0] = 1
        self.observation1[1, 1] = 2

        self.hs2 = BattleshipHypothesisSpace(grid_size=2, ship_labels=[1], 
            ship_sizes=[2], orientations=['V', 'H'])

        self.hs3 = BattleshipHypothesisSpace(grid_size=6, ship_labels=[1, 2, 3], 
            ship_sizes=[2, 3, 4], orientations=['V', 'H'])
        ## context 18 in paper
        self.observation2 = np.zeros((6, 6)) - 1
        self.observation2[1, 5] = self.observation2[2, 2] = self.observation2[3, 3] = self.observation2[4, 4:6] = 0
        self.observation2[4, 0:4] = 1
        self.observation2[2:4, 5] = 2
        self.observation2[1, 0] = 3
        

    def test_eig_simple_api(self):
        self.assertAlmostEqual(compute_eig_basic(self.hs1, "Red", self.observation1), 0)
        self.assertAlmostEqual(compute_eig_basic(self.hs1, "(any (map (lambda y0 (== (color y0) Red)) (set 1-1 1-2 1-3)))", self.observation1), 1)
        self.assertAlmostEqual(compute_eig_basic(self.hs1, "(size Red)", self.observation1), 0.81127812)


    def test_eig_full_api(self):
        belief = Bayes(self.hs1)
        context = Context(self.hs1, belief)
        context.observe(self.observation1)
        
        question = Parser.parse("Red")
        executor = Executor(question)
        eig = compute_eig(executor, context)
        # no IG for asking this question
        self.assertAlmostEqual(eig, 0)
        
        question = Parser.parse("(any (map (lambda y0 (== (color y0) Red)) (set 1-1 1-2 1-3)))")
        executor = Executor(question)
        eig = compute_eig(executor, context)
        # 4 valid hypothesis, 2 answers are True, 2 are False for this question
        # entropy([0.5, 0.5]) = 1
        self.assertAlmostEqual(eig, 1)
        
        question = Parser.parse("(size Red)")
        executor = Executor(question)
        eig = compute_eig(executor, context)
        # 4 valid hypothesis, 1 answers is 3, 3 are 2 for this question
        # entropy([0.25, 0.75]) = 2 - 0.75*log(3) = 0.81127812
        self.assertAlmostEqual(eig, 0.81127812)
        
        tmp_observation = self.observation1.copy()
        tmp_observation[1, 2] = 2
        context.observe(tmp_observation)
        eig = compute_eig(executor, context)
        # 1 valid hypothesis, answer is False
        # no IG for asking this question
        self.assertAlmostEqual(eig, 0)
        
        ## Simple example 2x2 grid with a single ship of lenth 2 => 4 hypotheses
        belief = Bayes(self.hs2)
        context = Context(self.hs2, belief)
        question = Parser.parse("(orient Blue)")
        executor = Executor(question)
        eig = compute_eig(executor, context)
        self.assertAlmostEqual(eig, 1)
        
        ## Full hypothesis space
        prior = EqualSizesDistribution(ship_labels=[1, 2, 3])
        belief = Bayes(self.hs3, prior)
        context = Context(self.hs3, belief)
        context.observe(self.observation2)
        question = Parser.parse("(bottomright (coloredTiles Purple))")
        executor = Executor(question)
        eig = compute_eig(executor, context)
        self.assertAlmostEqual(eig, 2.4275116)  # should pass once the prior is uniform over ship sizes
        
        question = Parser.parse("(size Purple)")
        executor = Executor(question)
        eig = compute_eig(executor, context)
        self.assertAlmostEqual(eig, 1.5653360)  # should pass once the prior is uniform over ship sizes
        
        question = Parser.parse("(color 3-1)")
        executor = Executor(question)
        eig = compute_eig(executor, context)
        self.assertAlmostEqual(eig, 0.9989968)