def main(fh, window_size=1):
    it = map(int, fh)
    window = [next(it) for _ in range(window_size)]
    answer = 0
    for num in it:
        if num > window[0]:
            answer += 1
        window = window[1:] + [num]

    return answer


if __name__ == "__main__":
    with open("data/1") as fh:
        print(main(fh, 1))

    with open("data/1") as fh:
        print(main(fh, 3))
