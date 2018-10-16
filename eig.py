subset
belief

belief_subset = belief[subset]
hypotheses_subset = hypotheses[subset]

'''
EIG for deterministic questions
'''

answers = run_program(program, hypotheses_subset)

p = []...
for answer in unique(answers):
    for i in enumerate(hypotheses_subset):
        if ansers[i] == answer:
            p[answer] += belief_subset[i]

EIG = entropy(p)


def entropy(x):
    - sum([p * log(p, 2) for p in x])
