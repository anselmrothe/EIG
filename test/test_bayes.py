import unittest
import numpy

import eig.bayes


class TestParser(unittest.TestCase):

    def test_normalize(self):
        self.assertEqual(normalize([1]), [1])
        self.assertEqual(normalize([1, 1]), [.5, .5])
        self.assertEqual(normalize([1, 4]), [.2, .8])
        self.assertEqual(normalize([0]), [0])
        self.assertEqual(normalize([0, 0]), [0, 0])
