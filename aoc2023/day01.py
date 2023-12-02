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


def get_first(text: str) -> str:
    ltext = ""
    for ch in text:
        if ch.isdigit():
            return int(ch)
        ltext += ch
        for num in _NUMBERS:
            if ltext.endswith(num):
                return _NUMBERS[num]


def get_last(text: str) -> str:
    rtext = ""
    for ch in reversed(text):
        if ch.isdigit():
            return int(ch)
        rtext = ch + rtext
        for num in _NUMBERS:
            if rtext.startswith(num):
                return _NUMBERS[num]


def main(data) -> None:
    total = 0

    for line in data:
        first = get_first(line)
        last = get_last(line)
        calib = (10 * first) + last
        total += calib

    print(total)


if __name__ == "__main__":
    main(get_input(day=1).splitlines())
