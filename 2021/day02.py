def part_a(fh):
    fwd = 0
    up = 0
    down = 0
    for row in fh:
        direction, dist = row.split()
        dist = int(dist)
        if direction == "forward":
            fwd += dist
        elif direction == "down":
            down += dist
        else:
            up += dist

    return fwd * (down - up)


def part_b(fh):
    x = 0
    y = 0
    aim = 0
    for row in fh:
        direction, dist = row.split()
        dist = int(dist)
        if direction == "forward":
            x += dist
            y += aim * dist
        elif direction == "down":
            aim += dist
        else:
            aim -= dist

    return x * y


if __name__ == "__main__":
    from aocutils import run

    run(part_a)
    run(part_b)
