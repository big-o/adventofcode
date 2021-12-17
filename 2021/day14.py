"""
Brute forcing involves going through the string linearly, but each step grows the string
exponentially.

Instead, just think of the string as a bag of pairs. We know that each pair that hits on
a rule can be replaced with two new pairs that can be defined by the rules provided, so
we simply look through our pair counts, set anything found in the rules to zero and
replace it with the same number of each new pair.

The tricky bit comes from converting our pair counts back into the original element
counts. Each element will appear twice (once in each pair it belongs to), so it will
always appear an even number of times when looking at the pairs. We therefore need to
half all the counts. The exceptions to this are the first and last element in the
sequence, which can be identified by always having an odd count. We therefore should
round *up* anything with an odd count. This isn't helped by the fact that Python's
`round()` function does *Bankers rounding* (https://stackoverflow.com/a/33019948/1959297).
"""
from collections import Counter


def load(fh):
    tmp = next(fh).strip()
    next(fh)

    rules = {}
    for line in fh:
        line = line.strip()
        rules[line[:2]] = [f"{line[0]}{line[-1]}", f"{line[-1]}{line[1]}"]

    template = Counter([tmp[i : i + 2] for i in range(len(tmp) - 1)])
    return template, rules


def pairs2elements(pairs):
    els = Counter()
    for pair, count in pairs.items():
        for el in pair:
            els[el] += count

    for el in els:
        # End elements will be odd due to the extra one, so round up.
        els[el] = int((els[el] / 2) + 0.5)
    return els


def main(fh, n_steps):
    template, rules = load(fh)
    for _ in range(n_steps):
        diff = Counter()
        for pair in rules:
            if pair in template:
                diff[pair] += template[pair]

        # Elements are inserted simultaneously, so do this step before all insertions.
        for pair in diff:
            template[pair] = 0

        for pair in diff:
            for newpair in rules[pair]:
                template[newpair] += diff[pair]

    els = pairs2elements(template).most_common()

    return els[0][1] - els[-1][1]


if __name__ == "__main__":
    from aocutils import run

    run(main, 10)
    run(main, 40)
