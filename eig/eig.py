import numpy as np
from .battleship import Parser, Executor, BattleshipHypothesisSpace
from .hypothesis import HypothesisSpace
from .context import Context

try:
    from math import log2
except ImportError:
    from math import log
    def log2(x):
        return log(x, 2)

def entropy(x):
    return - sum([p * log2(p) for p in x])

def compute_eig(executor: Executor, context: Context):
    """
    Compute EIG using executor and context.
    For deterministic questions with finite discrete set of answers:
        EIG = entropy(p(d))
    """
    answers, beliefs = context.get_answers(executor)
    answer_probs = {}
    for ans, belief in zip(answers, beliefs):
        if not ans in answer_probs:
            answer_probs[ans] = 0.
        answer_probs[ans] += belief
    return entropy(answer_probs.values())

def compute_eig_basic(hypotheses: HypothesisSpace, program: str, board: np.ndarray):
    """
    Compute EIG using hypothesis space, program string, and board.
    This method assumes all hypotheses are uniformly distributed.
    """
    question = Parser.parse(program)
    executor = Executor(question)
    valid_ids = hypotheses.observe(board)
    answers = hypotheses.execute_on_subspace(executor, valid_ids)
    single_prob = 1 / len(valid_ids)
    answer_probs = {}
    for ans in answers:
        if not ans in answer_probs:
            answer_probs[ans] = 0.
        answer_probs[ans] += single_prob
    return entropy(answer_probs.values())

def compute_eig_fast(program: str, board: np.ndarray, **kwargs):
    """
    A fast API for computing EIG. This will deduce valid hypotheses from the board, and
    execute the program on the board. Assumes all hypotheses are uniformly distributed.
    """
    question = Parser.parse(program)
    executor = Executor(question)
    hypotheses = BattleshipHypothesisSpace(**kwargs, observation=board)
    if len(hypotheses) == 0:
        return 0
    answers = hypotheses.execute_on_subspace(executor, range(len(hypotheses)))
    single_prob = 1 / len(hypotheses)
    answer_probs = {}
    for ans in answers:
        if not ans in answer_probs:
            answer_probs[ans] = 0.
        answer_probs[ans] += single_prob
    return entropy(answer_probs.values())