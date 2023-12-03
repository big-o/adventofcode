from dataclasses import dataclass
from typing import List, Tuple

from common import get_input


@dataclass
class Bag:
    red: int
    green: int
    blue: int

    def has(self, count: int, colour: str) -> bool:
        return count <= getattr(self, colour)

    def power(self) -> int:
        return self.red * self.green * self.blue


class Game:
    def __init__(self, data: str) -> None:
        game, draws = data.split(": ", 1)
        self.id = int(game[5:])
        self._draws = draws.split("; ")

    def play(self) -> List[Tuple[int, str]]:
        for draw in self._draws:
            for cubes in draw.split(", "):
                count, colour = cubes.split(" ", 1)
                yield (int(count), colour)

    def could_come_from(self, bag: Bag) -> bool:
        for count, colour in self.play():
            if not bag.has(count, colour):
                return False

        return True
    
    def get_min_bag(self) -> Bag:
        r, g, b = 0, 0, 0
        for count, colour in self.play():
            if colour == "red":
                r = max(r, count)
            elif colour == "green":
                g = max(g, count)
            elif colour == "blue":
                b = max(b, count)

        return Bag(r, g, b)


def main(data) -> None:
    bag = Bag(red=12, green=13, blue=14)

    possible = power = 0
    for line in data:
        game = Game(line)
        if game.could_come_from(bag):
            possible += game.id
        power += game.get_min_bag().power()

    print(possible)
    print(power)


if __name__ == "__main__":
    main(get_input(day=2).splitlines())
