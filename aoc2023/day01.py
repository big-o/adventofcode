from typing import Dict

from common import get_input


_NUMBERS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

_RNUMBERS = {word[::-1]: num for word, num in _NUMBERS.items()}


def get_first(text: str, numbers: Dict[str, int]) -> str:
    ltext = ""
    for ch in text:
        if ch.isdigit():
            return int(ch)
        ltext += ch
        for num in numbers:
            if ltext.endswith(num):
                return numbers[num]


def main(data) -> None:
    total = 0

    for line in data:
        first = get_first(line, _NUMBERS)
        last = get_first(reversed(line), _RNUMBERS)
        calib = (10 * first) + last
        total += calib

    print(total)


if __name__ == "__main__":
    main(get_input(day=1).splitlines())
