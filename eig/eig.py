from .battleship import Parser, Executor
try:
    from math import log2
except ImportError:
    from math import log
    def log2(x):
        return log(x, 2)

def entropy(x):
    return - sum([p * log2(p) for p in x])

def compute_eig(executor, context):
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

def compute_eig_basic(hypotheses, program, board):
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