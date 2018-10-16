import numpy
grid_size = 3
board = numpy.zeros((grid_size, grid_size))
board[(1, 1)] = -1
partly_reveald_board = board


h = numpy.zeros((grid_size, grid_size))
h[0, 0:2] = 1
h[1, 0:2] = 2
h[2, 0:2] = 3
does_match = match(h, partly_reveald_board)

bayes = Bayes()
bayes.belief = bayes.update_belief_subset(subset)


def bayes.update_belief_subset(subset):
    self.belief[!subset] = 0
    self.belief = self.normalize(self.belief)
