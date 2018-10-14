import unittest
import numpy

from eig.battleship import Ship, BattleshipHypothesis
from eig.question import Parser, Executor
from eig.question.program import ProgramSyntaxError

class TestParser(unittest.TestCase):

    def test_parse_error(self):
        with self.assertRaises(ProgramSyntaxError) as cm:
            question = Parser.parse("(== (color 1-1) Blu)")
        exception = cm.exception
        self.assertEqual(exception.error_msg, "Unrecognized token")

        with self.assertRaises(ProgramSyntaxError) as cm1:
            question = Parser.parse("(== (color 1-1 2-2) Blue)")
        exception = cm1.exception
        self.assertEqual(exception.error_msg, "Operand number mismatch. 1 expected, found 2")

        with self.assertRaises(ProgramSyntaxError) as cm2:
            question = Parser.parse("(== (color Red) Blue)")
        exception = cm2.exception
        self.assertEqual(exception.error_msg, "Parameter type mismatch")

    def test_parse_basic(self):
        question = Parser.parse("(== (color 1-1) Blue)")
        reference = {'type': 'equal',
                     'childs': [
                         {'type': 'color_fn',
                          'childs': [
                              {'type': 'location',
                              'value': (0, 0)}
                          ]},
                         {'type': 'color',
                          'value': 1}
                     ]}
        self.assertEqual(question.to_dict(), reference)