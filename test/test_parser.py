import unittest
import numpy

from eig.battleship import Ship, BattleshipHypothesis, \
                Parser, Executor
from eig.battleship.program import ProgramSyntaxError

class TestParser(unittest.TestCase):

    def test_parse_basic(self):
        question = Parser.parse("(== (color 1-1) Blue)")
        reference = {'type': 'equal',
                     'children': [
                         {'type': 'color_fn',
                          'children': [
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
        question = Parser.parse("(any (map (lambda x (== (orient x) H)) (set AllColors)))")
        reference = {
                'type': 'any_op',
                'children': [
                    {'type': 'map_op',
                     'children': [
                        {'type': 'lambda_op',
                         'children': [
                            {'type': 'lambda_x'},
                            {'type': 'equal',
                             'children': [
                                {'type': 'orient_fn',
                                 'children': [ {'type': 'lambda_x'} ]
                                },
                                {'type': 'orientation', 'value': 'H'}
                             ]}
                         ]},
                        {'type': 'set_op',
                         'children': [
                            {'type': 'set_color', 'value': 'AllColors'}
                         ]}
                     ]}
                ]}
        self.assertEqual(question.to_dict(), reference)
    
    def test_parse_error_basic(self):
        with self.assertRaises(ProgramSyntaxError) as cm:
            question = Parser.parse("(map (lambda x (+ 1 2)) (set AllColors))")
        exception = cm.exception
        self.assertEqual(exception.error_msg, "Top level type cannot be DataType.SET_N")

        with self.assertRaises(ProgramSyntaxError) as cm:
            question = Parser.parse("(any (map (lambda x (== (color y) Red)) (set AllColors)))")
        exception = cm.exception
        self.assertEqual(exception.error_msg, "DataType.LAMBDA_Y should not exist in lambda expression of DataType.LAMBDA_X")

        with self.assertRaises(ProgramSyntaxError) as cm:
            question = Parser.parse("(any (map (lambda x (== (orient x) H)) (set AllTiles)))")
        exception = cm.exception
        self.assertEqual(exception.error_msg, "Parameter type mismatch. "
            "Expected one of\n  (DataType.LAMBDA_FXB, DataType.SET_S),\n  (DataType.LAMBDA_FYB, DataType.SET_L),\n"
            "  (DataType.LAMBDA_FXL, DataType.SET_S),\n  (DataType.LAMBDA_FXN, DataType.SET_S),\nget (DataType.LAMBDA_FXB, DataType.SET_L)")

    def _test_optimization(self):   # TODO: Fix this
        question = Parser.parse("(bottomright (set AllTiles))", optimization=True)
        ref = {'type': 'location', 'value': (5, 5)}
        self.assertEqual(question.to_dict(), ref)
    
        question = Parser.parse("(and (all (map (lambda y (== (color y) Red)) (set AllTiles))) FALSE)", optimization=True)
        ref = {'type': 'boolean', 'value': False}
        self.assertEqual(question.to_dict(), ref)

        question = Parser.parse("(== (topleft (coloredTiles Blue)) (bottomright (set AllTiles)))", optimization=True)
        ref = {'type': 'equal',
               'children': [
                    {'type': 'topleft',
                     'children': [
                        {'type': 'colored_tiles_fn',
                         'children':[
                            {'type': 'color', 'value': 1}
                         ]}
                    ]},
                    {'type': 'location', 'value': (5, 5)}
               ]}
        self.assertEqual(question.to_dict(), ref)
        
        question = Parser.parse("(topleft (union (map (lambda x 1-1) (set AllColors)) (coloredTiles Blue)))", optimization=True)
        ref = {'type': 'topleft',
               'children': [
                    {'type': 'union',
                     'children': [
                        {'type': 'set_op',
                         'children':[
                             {'type': 'location', 'value': (0, 0)},
                             {'type': 'location', 'value': (0, 0)},
                             {'type': 'location', 'value': (0, 0)}
                         ]},
                        {'type': 'colored_tiles_fn',
                         'children': [
                             {'type': 'color', 'value': 1}
                         ]}
                    ]}
               ]}
        self.assertEqual(question.to_dict(), ref)

        question = Parser.parse("(++ (map (lambda x (+ 1 1)) (set AllColors)))", optimization=True)
        ref = {'type': 'number', 'value': 6}
        self.assertEqual(question.to_dict(), ref)