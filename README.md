# Question Programs & Expected Information Gain

To compile and run all unit tests:
`
python setup.py test
`

## EIG

- eig = EIG(question, context)


## Context

- context = Context(partly_revealed_board, hypotheses, belief)
  - subset of hypotheses
  - updated belief distribution


## Hypothesis

- hypothesis = Hypothesis(features)
- hypotheses = HypothesisSpace(settings)


## Belief

- bayes = Bayes(hypotheses)
- belief = bayes.prior()


## Question program

- question = Question("(size Red)")
