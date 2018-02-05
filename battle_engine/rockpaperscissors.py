""" Engine implementation for Rock, Paper, Scissors """
from numpy.random import uniform


class RPSEngine:
    def run(self, player1, player2):
        """ Run a game of Rock, Paper, Scissors """
        p1_move = player1.make_move()
        p2_move = player2.make_move()

        if p1_move == p2_move:
            return uniform() > 0.5
        elif p1_move - p2_move == 1:
            return 1
        else:
            return 0