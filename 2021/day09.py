from collections import deque


def load(fh):
    data = [[int(x) for x in line.strip()] for line in fh]
    shape = len(data), len(data[0])
    return data, shape


def neighbours(i, j, shape):
    if i > 0:
        yield i - 1, j
    if i < shape[0] - 1:
        yield i + 1, j
    if j > 0:
        yield i, j - 1
    if j < shape[1] - 1:
        yield i, j + 1


def is_lowpoint(data, shape, i, j):
    val = data[i][j]
    for n_i, n_j in neighbours(i, j, shape):
        if data[n_i][n_j] <= val:
            return False

    return True


def part_a(fh):
    data, shape = load(fh)
    risk = 0

    for i in range(shape[0]):
        for j in range(shape[1]):
            if is_lowpoint(data, shape, i, j):
                risk += data[i][j] + 1

    return risk


def part_b(fh):
    data, shape = load(fh)
    basins = {}

    for i in range(shape[0]):
        for j in range(shape[1]):
            if is_lowpoint(data, shape, i, j):
                basins[(i, j)] = set()

    for lowpoint, basin in basins.items():
        visited = []
        stack = deque([lowpoint])
        while stack:
            i, j = stack.popleft()
            if (i, j) in visited:
                continue

            if data[i][j] < 9:
                basin.add((i, j))
                for n_i, n_j in neighbours(i, j, shape):
                    stack.append((n_i, n_j))

            if (i, j) not in stack:
                visited.append((i, j))

    bsizes = sorted([len(basin) for basin in basins.values()])

    answer = 1
    for sz in bsizes[-3:]:
        answer *= sz
    return answer


if __name__ == "__main__":
    from aocutils import run

    run(part_a)
    run(part_b)
