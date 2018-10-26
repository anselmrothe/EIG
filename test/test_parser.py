import unittest
import numpy

from eig.battleship import Ship, BattleshipHypothesis, \
                Parser, Executor
from eig.battleship.question.program import ProgramSyntaxError

class TestParser(unittest.TestCase):

    def test_parse_basic(self):
        question = Parser.parse("(== (color 1-1) Blue)")
        reference = {'type': 'equal',
                     'childs': [
                         {'type': 'color_fn',
                          'childs': [
                              {'type': 'location', 'value': (0, 0)}
                          ]},
                         {'type': 'color', 'value': 1}
                     ]}
        self.assertEqual(question.to_dict(), reference)

    def test_parse_error_basic(self):
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
        self.assertEqual(exception.error_msg, "Parameter type mismatch. "
            "Expected DataType.LOCATION for parameter 1, get DataType.COLOR")


    def test_parse_lambda(self):
        question = Parser.parse("(any (map (lambda x (== (orient x) H)) (set Blue Red Purple)))")
        reference = {
                'type': 'any',
                'childs': [
                    {'type': 'map',
                     'childs': [
                        {'type': 'lambda',
                         'childs': [
                            {'type': 'lambda_x'},
                            {'type': 'equal',
                             'childs': [
                                {'type': 'orient_fn',
                                 'childs': [ {'type': 'lambda_x'} ]
                                },
                                {'type': 'orientation', 'value': 'H'}
                             ]}
                         ]},
                        {'type': 'set',
                         'childs': [
                            {'type': 'color', 'value': 1},
                            {'type': 'color', 'value': 2},
                            {'type': 'color', 'value': 3}
                         ]}
                     ]}
                ]}
        self.assertEqual(question.to_dict(), reference)
    
    def test_parse_error_basic(self):
        with self.assertRaises(ProgramSyntaxError) as cm:
            question = Parser.parse("(map (lambda x (+ 1 2)) (set Blue Red Purple))")
        exception = cm.exception
        self.assertEqual(exception.error_msg, "Top level type cannot be DataType.SET_N")

        with self.assertRaises(ProgramSyntaxError) as cm:
            question = Parser.parse("(any (map (lambda x (== (color y) Red)) (set Blue Red Purple)))")
        exception = cm.exception
        self.assertEqual(exception.error_msg, "DataType.LAMBDA_Y should not exist in lambda expression of DataType.LAMBDA_X")

        with self.assertRaises(ProgramSyntaxError) as cm:
            question = Parser.parse("(any (map (lambda x (== (orient x) H)) (set 1-1 1-2 1-3)))")
        exception = cm.exception
        self.assertEqual(exception.error_msg, "Parameter type mismatch. "
            "Expected one of\n  (DataType.LAMBDA_FXB, DataType.SET_S),\n  (DataType.LAMBDA_FYB, DataType.SET_L),\n"
            "  (DataType.LAMBDA_FXL, DataType.SET_S),\n  (DataType.LAMBDA_FXN, DataType.SET_S),\nget (DataType.LAMBDA_FXB, DataType.SET_L)")
