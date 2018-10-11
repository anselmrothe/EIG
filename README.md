# Question Programs & Expected Information Gain

To run all unit tests:
`
python -m unittest discover -v
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
