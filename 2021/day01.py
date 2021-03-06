from collections import deque


def main(fh, window_size=1):
    it = map(int, fh)
    try:
        window = deque([next(it) for _ in range(window_size)])
    except StopIteration:
        raise ValueError(f"Window size {window_size} must be smaller than input.")

    answer = 0
    for num in it:
        if num > window.popleft():
            answer += 1
        window.append(num)

    return answer


if __name__ == "__main__":
    from aocutils import run

    run(main, 1)
    run(main, 3)
