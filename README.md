# Question Programs & Expected Information Gain

This is a package for parsing/executing questions and calculating Expected Information Gain (EIG) for question programs defined on the Battleship Dataset in the paper "[Question Asking as Program Generation](https://arxiv.org/abs/1711.06351)".

This package provide a Pure python version (slow) and a Python/C++ hybrid version (fast). Both versions have the same API but different implementations.

## Installation

This package can be installed using pip
```
pip install expected-information-gain
```

## Basic Usage

The following example shows how to execute a program on a given board
```python
# define a board using BattleshipHypothesis
from eig.battleship import Ship, BattleshipHypothesis, Parser, Executor
ships = [Ship(ship_label=1, topleft=(0, 0), size=2, orientation='V'),
             Ship(ship_label=2, topleft=(1, 2), size=2, orientation='V')
hypothesis = BattleshipHypothesis(grid_size=3, ships=ships)
# the board looks like this
# B W W
# B W R
# W W R

# parse and execute the program
question = Parser.parse("(bottomright (coloredTiles Red))")
executor = Executor(question)
executor.execute(hypothesis)    # (2, 2)

# we can also evaluate general arithmic and logical expressions, with whatever hypothesis provided
question2 = Parser.parse("(and (not (< 4 9)) (== (+ 1 3) 4))")
executor2 = Executor(question)
executor.execute(hypothesis)    # False
```

The next example shows how to calculate Expected Information Gain on a partly revealed board
```python
# first we need to construct a hypothesis space 
# We suggest to do this as an initialization step, and use this instance every time
# Because this step is time consuming, and may take several seconds to finish.
from eig.battleship import BattleshipHypothesisSpace
hypotheses = BattleshipHypothesisSpace(grid_size=6, ship_labels=[1, 2, 3], 
            ship_sizes=[2, 3, 4], orientations=['V', 'H'])
            
# suppose we have a program and a partly revealed board
import numpy as np
program = "..."
board = np.array([...])

# next we can calculate EIG as follows
from eig import compute_eig_basic
from eig.battleship.program import ProgramSyntaxError
try:
    score = compute_eig_basic(hypotheses, program, board)
except ProgramSyntaxError:          # if the program is invalid, a ProgramSyntaxError will be raised
    # do something
except RuntimeError:                # if error happens during execution, a RuntimeError will be raised
    # do something
```

## Advanced Usage

We also provide some advanced interfaces, which are more efficient when the users need to calculate EIG for many 
programs on one given board, and they also allows users to incorporate more complicated distributions.

```python
# construct the hypothesis space
from eig.battleship import BattleshipHypothesisSpace
hypotheses = BattleshipHypothesisSpace(grid_size=6, ship_labels=[1, 2, 3], 
            ship_sizes=[2, 3, 4], orientations=['V', 'H'])

# calculate EIG as follows
from eig import compute_eig, Bayes, Context
from eig.battleship import Parser, Executor
from eig.battleship.program import ProgramSyntaxError
try:
    ast = Parser.parse(program)     # parse the program into abstract syntax tree
    executor = Executor(ast)        # obtain an executor to execute the program
    prior = EqualSizesDistribution(ship_labels=[1, 2, 3])   # a more cognitive inspired prior distribution
    belief = eig.Bayes(hypotheses, prior)       # a prior belief given the hypothesis space
    context = eig.Context(hypotheses, belief)   # context stores the posterior belief
    context.observe(board)                      # update posterior belief given the board
    score = eig.compute_eig(executor, context)  # compute EIG given program and posterior belief
except ProgramSyntaxError:          # if the program is invalid, a ProgramSyntaxError will be raised
    # do something
except RuntimeError:                # if error happens during execution, a RuntimeError will be raised
    # do something
```