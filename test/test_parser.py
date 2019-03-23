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
        question = Parser.parse("(any (map (lambda x0 (== (orient x0) H)) (set AllColors)))")
        reference = {
                'type': 'any_op',
                'children': [
                    {'type': 'map_op',
                     'children': [
                        {'type': 'lambda_op',
                         'children': [
                            {'type': 'lambda_x', 'value': 'x0'},
                            {'type': 'equal',
                             'children': [
                                {'type': 'orient_fn',
                                 'children': [ {'type': 'lambda_x', 'value': 'x0'} ]
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
    
    def test_parse_error_lambda(self):
        with self.assertRaises(ProgramSyntaxError) as cm:
            question = Parser.parse("(map (lambda x0 (+ 1 2)) (set AllColors))")
        exception = cm.exception
        self.assertEqual(exception.error_msg, "Top level type cannot be DataType.SET_N")

        with self.assertRaises(ProgramSyntaxError) as cm:
            question = Parser.parse("(any (map (lambda x1 (== (color x2) Red)) (set AllColors)))")
        exception = cm.exception
        self.assertEqual(exception.error_msg, "Lambda variable x2 should not exist here")

        with self.assertRaises(ProgramSyntaxError) as cm:
            question = Parser.parse("(++ (map (lambda x1 (== (size x1) (++ (map (lambda x1 (== (orient x1) V)) (set AllColors))))) (set AllColors)))")
        exception = cm.exception
        self.assertEqual(exception.error_msg, "Lambda variable x1 has already been defined")

        with self.assertRaises(ProgramSyntaxError) as cm:
            question = Parser.parse("(any (map (lambda x2 (== (orient x2) H)) (set AllTiles)))")
        exception = cm.exception
        self.assertEqual(exception.error_msg, "Parameter type mismatch. "
            "Expected one of\n  (DataType.LAMBDA_FXB, DataType.SET_S),\n  (DataType.LAMBDA_FYB, DataType.SET_L),\n"
            "  (DataType.LAMBDA_FXL, DataType.SET_S),\n  (DataType.LAMBDA_FXN, DataType.SET_S),\nget (DataType.LAMBDA_FXB, DataType.SET_L)")

        with self.assertRaises(ProgramSyntaxError) as cm:
            question = Parser.parse("(++ (lambda (lambda x0 (size x0)) (set AllColors)))")
        exception = cm.exception
        self.assertEqual(exception.error_msg, "Parameter type mismatch. "
            "The first child of lambda operator should be lambda\n"
            "variable (x0, x1, y2, etc.), get lambda_op")


    def test_optimization(self):
        question = Parser.parse("(bottomright (set AllTiles))", optimization=True)
        ref = {'type': 'location', 'value': (5, 5)}
        self.assertEqual(question.to_dict(), ref)
    
        question = Parser.parse("(and (all (map (lambda y0 (== (color y0) Red)) (set AllTiles))) FALSE)", optimization=True)
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
        
        question = Parser.parse("(topleft (union (map (lambda x0 1-1) (set AllColors)) (coloredTiles Blue)))", optimization=True)
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

        question = Parser.parse("(++ (map (lambda x0 (+ 1 1)) (set AllColors)))", optimization=True)
        ref = {'type': 'number', 'value': 6}
        self.assertEqual(question.to_dict(), ref)