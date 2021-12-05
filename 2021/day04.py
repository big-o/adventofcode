import numpy as np


class Bingo:
    """
    Rewrite the bingo boards, replacing each number with it's order in the random draw
    shuffle.

    Now we can simply check if someone has won each round by comparing the max value on
    each row/column to the draw index.
    """

    def __init__(self, data):
        self.rvs = np.array([int(x) for x in next(data).split(",")])
        order = {rv: i for i, rv in enumerate(self.rvs)}

        boards = []
        rboards = []
        board = []
        for line in data:
            line = [int(n) for n in line.split()]
            if line:
                board.append(line)
                if len(line) == len(board):
                    boards.append(board)
                    rboards.append([[order[n] for n in row] for row in board])
                    board = []

        self.boards = np.array(boards)
        self.rboards = np.array(rboards)

    def score(self, board, rnd):
        return (
            np.where(np.isin(board, self.rvs[: rnd + 1]), 0, board).sum()
            * self.rvs[rnd]
        )

    def play_to_win(self):
        """
        Check at each step if any row/col is all less than the current index.
        This represents a winning row.
        """
        for rnd in range(self.boards.shape[1], len(self.rvs)):
            bingo = np.max(self.rboards.max(axis=-2) <= rnd, axis=1) | np.max(
                self.rboards.max(axis=-1) <= rnd, axis=1
            )
            if np.any(bingo):
                winner = np.where(bingo)[0]
                return self.score(self.boards[winner], rnd)

    def play_to_lose(self):
        "Work backwards using our shuffle order and find the first board to lose."
        for rnd in range(len(self.rvs) - 1, self.boards.shape[1] - 1, -1):
            bingo = np.max(self.rboards.max(axis=-2) <= rnd, axis=1) | np.max(
                self.rboards.max(axis=-1) <= rnd, axis=1
            )
            if not np.all(bingo):
                loser = np.where(~bingo)[0]
                return self.score(self.boards[loser], rnd + 1)


def main(fh):
    game = Bingo(fh)
    winning_score = game.play_to_win()
    losing_score = game.play_to_lose()
    return winning_score, losing_score


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    with open(filename) as fh:
        print(main(fh))
