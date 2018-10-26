from math import log


def log2(x):
    return log(x, 2)


def entropy(x):
    return - sum([p * log2(p) for p in x])

def compute_eig(executor, context):
    """
    Compute EIG for deterministic questions with finite discrete set of answers:
        EIG = entropy(p(d))
    """
    answers, beliefs = context.get_answers(executor)
    answer_probs = {}
    for ans, belief in zip(answers, beliefs):
        if not ans in answer_probs:
            answer_probs[ans] = 0.
        answer_probs[ans] += belief
    return entropy(answer_probs.values())