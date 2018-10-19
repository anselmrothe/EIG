import unittest
import numpy as np
from eig.bayes import normalize, Bayes


class TestBayes(unittest.TestCase):

    def test_normalize(self):
        self.assertTrue(np.array_equal(normalize(np.array([1])), np.array([1])))
        self.assertTrue(np.array_equal(normalize(np.array([1, 1])), np.array([.5, .5])))
        self.assertTrue(np.array_equal(normalize(np.array([1, 4])), np.array([.2, .8])))
        self.assertTrue(np.array_equal(normalize(np.array([0])), np.array([0])))
        self.assertTrue(np.array_equal(normalize(np.array([0, 0])), np.array([0, 0])))

    def test_prior(self):
        # note currently we only have uniform distribution
        belief = Bayes(4)
        self.assertTrue(np.array_equal(belief.belief, np.array([.25, .25, .25, .25])))

    def test_update(self):
        belief = Bayes(5)
        belief.update_belief([0, 3, 4])
        self.assertTrue(np.array_equal(belief.belief, np.array([0, .5, .5, 0, 0])))
