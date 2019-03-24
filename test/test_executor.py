import unittest
import numpy

from eig.battleship import Ship, BattleshipHypothesis, \
                Parser, Executor

class TestExecutor(unittest.TestCase):
    def setUp(self):
        self.empty_hypothesis = BattleshipHypothesis(grid_size=3, ships=[])

        ships1 = [Ship(ship_label=1, topleft=(0, 0), size=3, orientation='V'),
                 Ship(ship_label=2, topleft=(0, 1), size=2, orientation='H')]
        self.hypothesis1 = BattleshipHypothesis(grid_size=3, ships=ships1)

        ships2 = [Ship(ship_label=1, topleft=(0, 0), size=3, orientation='V'),
                 Ship(ship_label=2, topleft=(1, 1), size=2, orientation='V')]
        self.hypothesis2 = BattleshipHypothesis(grid_size=3, ships=ships2)

        ships3 = [Ship(ship_label=1, topleft=(0, 0), size=2, orientation='V'),
                 Ship(ship_label=2, topleft=(1, 2), size=2, orientation='V')]
        self.hypothesis3 = BattleshipHypothesis(grid_size=3, ships=ships3)

        ships4 = [Ship(ship_label=1, topleft=(0, 0), size=2, orientation='V'),
                 Ship(ship_label=2, topleft=(1, 2), size=2, orientation='H'),
                 Ship(ship_label=3, topleft=(0, 5), size=3, orientation='V')]
        self.hypothesis4 = BattleshipHypothesis(grid_size=6, ships=ships4)

        ships5 = [Ship(ship_label=1, topleft=(0, 0), size=2, orientation='V'),
                 Ship(ship_label=2, topleft=(2, 2), size=2, orientation='V'),
                 Ship(ship_label=3, topleft=(0, 5), size=3, orientation='V')]
        self.hypothesis5 = BattleshipHypothesis(grid_size=6, ships=ships5)


    def test_primitives(self):
        question1 = Parser.parse("Red")
        executor1 = Executor(question1)
        self.assertEqual(executor1.execute(self.empty_hypothesis), 2)

        question2 = Parser.parse("2-1")
        executor2 = Executor(question2)
        self.assertEqual(executor2.execute(self.empty_hypothesis), (1, 0))

        question3 = Parser.parse("H")
        executor3 = Executor(question3)
        self.assertEqual(executor3.execute(self.empty_hypothesis), "H")

        question4 = Parser.parse("6")
        executor4 = Executor(question4)
        self.assertEqual(executor4.execute(self.empty_hypothesis), 6)

    def test_basic(self):
        question1 = Parser.parse("(> 3 1)")
        executor1 = Executor(question1)
        self.assertTrue(executor1.execute(self.empty_hypothesis))

        question2 = Parser.parse("(== Water Water)")
        executor2 = Executor(question2)
        self.assertTrue(executor2.execute(self.empty_hypothesis))

        question3 = Parser.parse("(+ 2 5)")
        executor3 = Executor(question3)
        self.assertEqual(executor3.execute(self.empty_hypothesis), 7)

        question4 = Parser.parse("(and (not (< 4 9)) (== (+ 1 3) 4))")
        executor4 = Executor(question4)
        self.assertFalse(executor4.execute(self.empty_hypothesis))

    def test_board_funcs(self):
        question = Parser.parse("(== (color 1-1) Blue)")
        executor = Executor(question)
        self.assertTrue(executor.execute(self.hypothesis1))
        self.assertFalse(executor.execute(self.empty_hypothesis))

        question = Parser.parse("(== (orient Red) (orient Blue))")
        executor = Executor(question)
        self.assertFalse(executor.execute(self.hypothesis1))
        self.assertTrue(executor.execute(self.hypothesis2))

        question = Parser.parse("(touch Blue Red)")
        executor = Executor(question)
        self.assertTrue(executor.execute(self.hypothesis1))
        self.assertTrue(executor.execute(self.hypothesis2))
        self.assertFalse(executor.execute(self.hypothesis3))

        question = Parser.parse("(== (size Blue) 3)")
        executor = Executor(question)
        self.assertTrue(executor.execute(self.hypothesis1))
        self.assertFalse(executor.execute(self.hypothesis3))

        question = Parser.parse("(bottomright (coloredTiles Red))")
        executor = Executor(question)
        self.assertEqual(executor.execute(self.hypothesis1), (0, 2))
        self.assertEqual(executor.execute(self.hypothesis3), (2, 2))

    def test_set_operations(self):
        question = Parser.parse("(setSize (setDifference (set 1-1 1-2 1-3) (set 1-2 2-1)))")
        executor = Executor(question)
        self.assertEqual(executor.execute(self.empty_hypothesis), 2)

        question = Parser.parse("(setSize (union (set 1-1 1-2 1-3) (set 1-2 2-1)))")
        executor = Executor(question)
        self.assertEqual(executor.execute(self.empty_hypothesis), 4)

        question = Parser.parse("(setSize (intersection (set 1-1 1-2 1-3) (set 1-2 1-2 2-1)))")
        executor = Executor(question)
        self.assertEqual(executor.execute(self.empty_hypothesis), 1)

        question = Parser.parse("(setSize (union (set 1-1 1-3 1-2) (set 2-1 1-2 1-3)))")
        executor = Executor(question)
        self.assertEqual(executor.execute(self.empty_hypothesis), 4)

    def test_lambda_x(self):
        
        question = Parser.parse("(any (map (lambda x0 (== (orient x0) H)) (set AllColors)))")
        executor = Executor(question)
        self.assertTrue(executor.execute(self.hypothesis4))
        self.assertFalse(executor.execute(self.hypothesis5))

        # How many ships' sizes are the same as the number of vertical ships?
        question = Parser.parse("(++ (map (lambda x0 (== (size x0) (++ (map (lambda x1 (== (orient x1) V)) (set AllColors))))) (set AllColors)))")
        executor = Executor(question)
        self.assertEqual(executor.execute(self.hypothesis4), 2)
        self.assertEqual(executor.execute(self.hypothesis5), 1)


    def test_lambda_y(self):
        question = Parser.parse("(any (map (lambda y0 (and (== (color y0) Red) (== (rowL y0) 2))) (set AllTiles)))")
        executor = Executor(question)
        self.assertTrue(executor.execute(self.hypothesis4))
        self.assertFalse(executor.execute(self.hypothesis5))

    def test_runtime_error(self):
        with self.assertRaises(RuntimeError) as cm:
            question = Parser.parse("(size Purple)")
            executor = Executor(question)
            executor.execute(self.hypothesis1)

        with self.assertRaises(RuntimeError) as cm:
            question = Parser.parse("(touch Water (color 4-5))")
            executor = Executor(question)
            executor.execute(self.hypothesis4)
