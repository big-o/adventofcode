import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import coo_matrix


def load(fh):
    row, col, data = [], [], []
    instructions = []
    for line in fh:
        line = line.strip()
        if not line:
            break
        x, y = [int(n) for n in line.split(",")]
        row.append(x)
        col.append(y)
        data.append(1)

    ar = coo_matrix((data, (row, col))).toarray()
    for row in fh:
        txt, idx = row.strip().split("=")
        axis = 0 if txt[-1] == "x" else 1
        instructions.append((axis, int(idx)))

    return ar, instructions


def main(fh, steps=None, show=False):
    paper, instructions = load(fh)
    for i, (ax, idx) in enumerate(instructions, 1):
        if steps is not None and i > steps:
            break

        halves = (
            [paper[:idx, :], paper[idx + 1 :, :]]
            if ax == 0
            else [paper[:, :idx], paper[:, idx + 1 :]]
        )
        halves[1] = np.flip(halves[1], axis=ax)
        paper = halves[0] | halves[1]

    if show:
        plt.imshow(paper.T)
        plt.show()

    return paper.sum()


if __name__ == "__main__":
    from aocutils import run

    run(main, steps=1)
    run(main, show=True)
