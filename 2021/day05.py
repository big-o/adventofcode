from itertools import zip_longest
from collections import Counter
import re


def main(fh, diag=False):
    FMT = re.compile(r"^(\d+),(\d+) -> (\d+),(\d+)")
    ctr = Counter()

    for line in fh:
        x1, y1, x2, y2 = map(int, FMT.match(line).group(1, 2, 3, 4))
        if not diag and x1 != x2 and y1 != y2:
            # Skip diagonals
            continue

        dx = 1 if x2 >= x1 else -1
        dy = 1 if y2 >= y1 else -1
        for x, y in zip_longest(range(x1, x2 + dx, dx), range(y1, y2 + dy, dy)):
            x = x if x is not None else x2
            y = y if y is not None else y2
            ctr[(x, y)] += 1

    return len([pt for pt in ctr if ctr[pt] > 1])


if __name__ == "__main__":
    from aocutils import run

    run(main)
    run(main, diag=True)
