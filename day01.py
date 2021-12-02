import requests


def part_a(fh):
    it = map(int, fh)
    prev = next(it)
    answer = 0
    for curr in it:
        if curr > prev:
            answer += 1
        prev = curr

    return answer


def part_b(fh):
    it = map(int, fh)
    left, mid, right = next(it), next(it), next(it)
    answer = 0
    for num in it:
        if num > left:
            answer += 1
        left, mid, right = mid, right, num

    return answer


if __name__ == "__main__":
    with open("data/1") as fh:
        print(part_a(fh))

    with open("data/1") as fh:
        print(part_b(fh))
