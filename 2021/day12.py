from collections import Counter, defaultdict


class Graph:
    def __init__(self, fh):
        self.nodes = defaultdict(list)

        for line in fh:
            node_a, node_b = line.strip().split("-")
            self.add_edge(node_a, node_b)

    def add_edge(self, node_a, node_b):
        self.nodes[node_a].append(node_b)
        self.nodes[node_b].append(node_a)

    def count_paths(self, start="start", end="end", dbl=False):
        if dbl:
            paths = set()
            for node in self.nodes:
                if node not in (start, end):
                    paths.update(
                        [p for p in self.dfs([start], end, Counter(), dbl=node)]
                    )
        else:
            paths = set(self.dfs([start], end, Counter()))

        # for p in paths:
        #     print(",".join(p))

        return len(paths)

    def dfs(self, path, goal, visited, dbl=None):
        node = path[-1]
        if node == goal:
            yield tuple(path)
        else:
            if not node.isupper():
                visited[node] += 1
            for n in self.nodes[node]:
                if n not in visited or (n == dbl and visited[n] < 2):
                    yield from self.dfs(path + [n], goal, visited.copy(), dbl)


def main(fh, dbl=False):
    G = Graph(fh)
    return G.count_paths(dbl=dbl)


if __name__ == "__main__":
    from aocutils import run

    run(main)
    run(main, True)
