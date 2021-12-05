def part_a(fh):
    most_common = [0] * 12
    for num in fh:
        for pos, bit in enumerate(num.rstrip()):
            most_common[pos] += -1 if bit == "0" else 1

    gamma = 0
    for pos, bit in enumerate(most_common):
        gamma += min(max(0, bit), 1) << 11 - pos

    eps = ~gamma & 0xFFF
    return gamma * eps


### Boring solution ###


def get_rating(nums, idxs, rating, level=0):
    first = {0: [], 1: []}
    for idx in idxs:
        num = nums[idx]
        first[int(num[level])].append(idx)

    choice = 0 if len(first[1]) < len(first[0]) else 1
    if rating == "co2":
        choice = abs(choice - 1)

    idxs = first[choice]

    if not idxs:
        raise RuntimeError({k: len(v) for k, v in first.items()})
    elif len(idxs) == 1:
        return int(nums[idxs[0]], base=2)
    else:
        return get_rating(nums, idxs, rating, level + 1)


def part_b(fh):
    nums = [num.strip() for num in fh]
    idxs = list(range(len(nums)))
    o2 = get_rating(nums, idxs, "o2")
    fh.seek(0)
    co2 = get_rating(nums, idxs, "co2")

    print(o2, co2)
    return o2 * co2


### Contrived solution ###


class Node:
    def __init__(self, val):
        self.val = val
        self.zeros = None
        self.ones = None

    def __lt__(self, other):
        return other is not None and len(self.val) < len(other.val)


class Tree:
    def __init__(self, data):
        self.data = [num.rstrip() for num in data]
        self.root = self.insert(list(range(len(self.data))))

    def insert(self, idxs, level=0):
        if not idxs or level > 11:
            return None

        node = Node(idxs)
        if len(idxs) > 1:
            zeros = []
            ones = []
            for idx in idxs:
                if int(self.data[idx][level]):
                    ones.append(idx)
                else:
                    zeros.append(idx)

            node.zeros = self.insert(zeros, level + 1)
            node.ones = self.insert(ones, level + 1)

        return node

    def walk(self, prefer):
        node = self.root
        while node:
            result = node.val
            zeros = True if not node.ones or node.ones < node.zeros else False
            if prefer == 0:
                zeros = not zeros
            node = node.zeros if zeros else node.ones

        return int(self.data[result[0]], base=2)

    def o2(self):
        return self.walk(prefer=1)

    def co2(self):
        return self.walk(prefer=0)


def part_b_btree(fh):
    tree = Tree(fh)
    o2, co2 = tree.o2(), tree.co2()
    print(o2, co2)
    return o2 * co2


if __name__ == "__main__":
    import sys

    filename = "input/03"
    with open(filename) as fh:
        print(part_a(fh))

    with open(filename) as fh:
        print(part_b(fh))

    with open(filename) as fh:
        print(part_b_btree(fh))
