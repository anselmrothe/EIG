import unittest
import numpy

from eig.battleship import Ship, BattleshipHypothesis
from eig.question import Parser, Executor
from eig.question.program import ProgramSyntaxError

class TestParser(unittest.TestCase):

    def test_parse_error(self):
        with self.assertRaises(ProgramSyntaxError) as cm:
            question = Parser.parse("(= (color 1-1 2-2) Blue)")
        exception = cm.exception
        self.assertEqual(exception.error_msg, "Operand number mismatch. 1 expected, found 2")

    def test_parse_basic(self):
        question = Parser.parse("(= (color 1-1) Blue)")
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

    def test_execute(self):
        pass
        """
        question = Parser.parse("(= (color 1-1) Blue)")
        ships = [Ship(ship_label=1, topleft=(0, 0), size=3, orientation='vertical'),
                 Ship(ship_label=2, topleft=(0, 1), size=2, orientation='horizontal')]
        hypothesis = BattleshipHypothesis(grid_size=3, ships=ships)
        result = Executor.execute(question, hypothesis)
        reference = True"""