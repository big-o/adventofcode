def main(fh, t):
    fish = [0] * 9
    for ttl in [int(n) for line in fh for n in line.strip().split(",")]:
        fish[ttl] += 1

    for tick in range(t):
        fish = fish[1:] + [fish[0]]
        fish[6] += fish[-1]

    return sum(fish)


if __name__ == "__main__":
    from aocutils import run

    run(main, 18)
    run(main, 80)
    run(main, 256)
