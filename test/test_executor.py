import unittest
import numpy

from eig.battleship import Ship, BattleshipHypothesis
from eig.question import Parser, Executor

class TestParser(unittest.TestCase):

    def test_primitives(self):
        empty_hypothesis = BattleshipHypothesis(grid_size=3, ships=[])

        question1 = Parser.parse("Red")
        executor1 = Executor(question1)
        self.assertEqual(executor1.execute(empty_hypothesis), 2)

        question2 = Parser.parse("2-1")
        executor2 = Executor(question2)
        self.assertEqual(executor2.execute(empty_hypothesis), (1, 0))

        question3 = Parser.parse("H")
        executor3 = Executor(question3)
        self.assertEqual(executor3.execute(empty_hypothesis), "H")

        question4 = Parser.parse("6")
        executor4 = Executor(question4)
        self.assertEqual(executor4.execute(empty_hypothesis), 6)

    def test_basic(self):
        empty_hypothesis = BattleshipHypothesis(grid_size=3, ships=[])

        question1 = Parser.parse("(> 3 1)")
        executor1 = Executor(question1)
        self.assertTrue(executor1.execute(empty_hypothesis))

        question2 = Parser.parse("(== Water Water)")
        executor2 = Executor(question2)
        self.assertTrue(executor2.execute(empty_hypothesis))

        question3 = Parser.parse("(+ 2 5)")
        executor3 = Executor(question3)
        self.assertEqual(executor3.execute(empty_hypothesis), 7)

        question4 = Parser.parse("(and (not (< 4 9)) (== (+ 1 3) 4))")
        executor4 = Executor(question4)
        self.assertFalse(executor4.execute(empty_hypothesis))

    def test_color_fn(self):
        question = Parser.parse("(== (color 1-1) Blue)")
        executor = Executor(question)

        ships = [Ship(ship_label=1, topleft=(0, 0), size=3, orientation='vertical'),
                 Ship(ship_label=2, topleft=(0, 1), size=2, orientation='horizontal')]
        hypothesis = BattleshipHypothesis(grid_size=3, ships=ships)
        self.assertTrue(executor.execute(hypothesis))

        hypothesis2 = BattleshipHypothesis(grid_size=3, ships=[])
        self.assertFalse(executor.execute(hypothesis2))

    def test_orient_fn(self):
        question = Parser.parse("(== (orient Red) (orient Blue))")
        executor = Executor(question)

        ships1 = [Ship(ship_label=1, topleft=(0, 0), size=3, orientation='vertical'),
                 Ship(ship_label=2, topleft=(0, 1), size=2, orientation='horizontal')]
        hypothesis1 = BattleshipHypothesis(grid_size=3, ships=ships1)
        self.assertFalse(executor.execute(hypothesis1))

        ships2 = [Ship(ship_label=1, topleft=(0, 0), size=3, orientation='vertical'),
                 Ship(ship_label=2, topleft=(1, 1), size=2, orientation='vertical')]
        hypothesis2 = BattleshipHypothesis(grid_size=3, ships=ships2)
        self.assertTrue(executor.execute(hypothesis2))
