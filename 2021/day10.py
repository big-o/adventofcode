def part_a(fh):
    pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
    score = 0
    for line in fh:
        line = line.rstrip()
        stack = []
        for ch in line:
            if not stack or ch in pairs:
                stack.append(ch)
            else:
                prev = stack.pop()
                if pairs[prev] != ch:
                    score += scores[ch]

    return score


def part_b(fh):
    pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
    scores = {")": 1, "]": 2, "}": 3, ">": 4}
    linescores = []
    for line in fh:
        score = 0
        line = line.rstrip()
        stack = []
        corrupt = False
        for ch in line:
            if not stack or ch in pairs:
                stack.append(ch)
            else:
                prev = stack.pop()
                if pairs[prev] != ch:
                    corrupt = True
                    break

        if not corrupt:
            while stack:
                prev = stack.pop()
                score *= 5
                score += scores[pairs[prev]]

            linescores.append(score)

    return sorted(linescores)[len(linescores) // 2]


if __name__ == "__main__":
    from aocutils import run

    run(part_a)
    run(part_b)
