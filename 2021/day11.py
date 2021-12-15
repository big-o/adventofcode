from collections import deque
from rich import print as rprint


def load(fh):
    data = [[int(x) for x in line.strip()] for line in fh]
    shape = len(data), len(data[0])
    return data, shape


def neighbours(i, j, shape):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            n_i, n_j = i + dx, j + dy
            if 0 <= n_i < shape[0] and 0 <= n_j < shape[1] and (n_i, n_j) != (i, j):
                yield n_i, n_j


def display_data(data, stepno=None):
    if stepno is not None:
        print(f"Step {stepno}:")

    for row in data:
        rprint("".join(f"{o}" if o > 0 else f"[bold yellow]{o}[/]" for o in row))

    print("")


def step(data, shape, debug=False, stepno=None):
    charged = set()
    for i in range(shape[0]):
        for j in range(shape[1]):
            data[i][j] += 1
            if data[i][j] > 9:
                charged.add((i, j))

    flashes = set()
    for loc in charged:
        stack = deque([loc])
        while stack:
            i, j = stack.popleft()

            if data[i][j] > 9:
                data[i][j] = 0
                flashes.add((i, j))
                for n_i, n_j in neighbours(i, j, shape):
                    if (n_i, n_j) not in flashes:
                        data[n_i][n_j] += 1
                    if data[n_i][n_j] > 9:
                        stack.append((n_i, n_j))

    if debug:
        display_data(data, stepno)

    return len(flashes)


def part_a(fh, n, debug=False):
    data, shape = load(fh)
    if debug:
        display_data(data, 0)

    flashes = sum(step(data, shape, debug, i) for i in range(1, n + 1))
    return flashes


def part_b(fh):
    data, shape = load(fh)

    maxflash = shape[0] * shape[1]
    n = 1
    while step(data, shape) != maxflash:
        n += 1

    return n


if __name__ == "__main__":
    from aocutils import run

    # run(part_a, 10, debug=True)
    run(part_a, 100)
    run(part_b)
