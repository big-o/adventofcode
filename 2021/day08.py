from collections import defaultdict, Counter


def parse_input(fh):
    return [
        [tuple(map(set, l.split())) for l in line.strip().split("|")] for line in fh
    ]


def part_a(fh):
    inp = parse_input(fh)

    decoded = []
    answer = 0
    for signals, out in inp:
        for dig in out:
            if len(dig) in (2, 3, 4, 7):
                answer += 1

    return answer


def part_b(fh):
    inp = parse_input(fh)
    answer = 0
    for signals, out in inp:
        sizes = defaultdict(list)
        for sig in signals:
            sizes[len(sig)].append(sig)

        dec = {
            1: sizes[2][0],
            4: sizes[4][0],
            7: sizes[3][0],
            8: sizes[7][0],
        }

        n = (dec[7] - dec[1]).pop()
        cnts6 = Counter([ch for dig in sizes[5] for ch in dig])
        for ch in cnts6:
            if cnts6[ch] == 1:
                if ch in dec[4]:
                    nw = ch
                else:
                    sw = ch

        dec[3] = dec[8] - set([nw, sw])
        for dig in sizes[5]:
            if dig != dec[3]:
                if sw in dig:
                    dec[2] = dig
                else:
                    dec[5] = dig

        dec[6] = dec[5] | set([sw])
        mid = (dec[4] - dec[7] - set([nw])).pop()

        for dig in sizes[6]:
            if sw not in dig:
                dec[9] = dig
            elif mid not in dig:
                dec[0] = dig

        codes = {frozenset(v): k for k, v in dec.items()}
        num = 0
        for dig in out:
            num *= 10
            num += codes[frozenset(dig)]

        answer += num

    return answer


if __name__ == "__main__":
    from aocutils import run

    run(part_a)
    run(part_b)
