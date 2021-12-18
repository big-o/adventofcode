import networkx as nx


def neighbours(i, j, shape):
    if i > 0:
        yield i - 1, j
    if i < shape[0] - 1:
        yield i + 1, j
    if j > 0:
        yield i, j - 1
    if j < shape[1] - 1:
        yield i, j + 1


def l2(a, b):
    x1, y1 = a
    x2, y2 = b
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def make_grid(fh, tiles):
    tile = [[int(n) for n in line.strip()] for line in fh]
    tshape = len(tile), len(tile[0])

    data = [[0] * len(tile) * tiles for _ in range(len(tile[0]) * tiles)]
    for x in range(tiles):
        for y in range(tiles):
            shift = x + y
            for i in range(tshape[0]):
                for j in range(tshape[1]):
                    v = tile[i][j] + shift
                    data[i + x * tshape[0]][j + y * tshape[1]] = v % 10 + (
                        1 if v > 9 else 0
                    )

    shape = len(data), len(data[0])
    return data, shape


def main(fh, tiles):
    vals, shape = make_grid(fh, tiles)

    G = nx.DiGraph()
    for i in range(len(vals)):
        for j in range(len(vals[i])):
            for n_i, n_j in neighbours(i, j, shape):
                G.add_edge((i, j), (n_i, n_j), risk=vals[n_i][n_j])
                G.add_edge((n_i, n_j), (i, j), risk=vals[i][j])

    # Default method (Dijkstra) is too slow; define a heuristic and use A* instead.
    path = nx.astar_path(
        G, (0, 0), (shape[0] - 1, shape[1] - 1), heuristic=l2, weight="risk"
    )
    cost = sum(G.edges[path[i], path[i + 1]]["risk"] for i in range(len(path) - 1))
    return cost


if __name__ == "__main__":
    from aocutils import run

    for tiling in (1, 5):
        print(f"With x{tiling} tiling: ", end="")
        run(main, tiling)
