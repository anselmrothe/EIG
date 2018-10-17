import unittest
import numpy as np
from eig.bayes import normalize


class TestBayes(unittest.TestCase):

    def test_normalize(self):
        self.assertTrue(np.array_equal(normalize(np.array([1])), np.array([1])))
        self.assertTrue(np.array_equal(normalize(np.array([1, 1])), np.array([.5, .5])))
        self.assertTrue(np.array_equal(normalize(np.array([1, 4])), np.array([.2, .8])))
        self.assertTrue(np.array_equal(normalize(np.array([0])), np.array([0])))
        self.assertTrue(np.array_equal(normalize(np.array([0, 0])), np.array([0, 0])))

    # TODO: test bayes belief update