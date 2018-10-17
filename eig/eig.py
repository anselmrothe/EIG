from math import log2

def entropy(x):
    return - sum([p * log2(p) for p in x])

def compute_eig(executor, context):
    """
    Compute EIG for deterministic questions with finite discrete set of answers:
        EIG = entropy(p(d))
    """
    answers = {}
    for hypothesis, belief in context.hypotheses_subset():
        ans = executor.execute(hypothesis)
        if not ans in answers:
            answers[ans] = 0.
        answers[ans] += belief
    return entropy(answers.values())