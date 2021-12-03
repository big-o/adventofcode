def main(fh, window_size=1):
    it = map(int, fh)
    try:
        window = [next(it) for _ in range(window_size)]
    except StopIteration:
        raise ValueError(f"Window size {window_size} must be smaller than input.")

    answer = 0
    for num in it:
        if num > window[0]:
            answer += 1
        window = window[1:] + [num]

    return answer


if __name__ == "__main__":
    import sys

    filename = "data/01"
    with open(filename) as fh:
        print(main(fh, 1))

    with open(filename) as fh:
        print(main(fh, 3))

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            with open(filename) as fh:
                print(main(fh, int(arg)))
