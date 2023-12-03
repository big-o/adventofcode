"""
Common I/O utils for AOC challenges.

Create a file called .config.json in the same location as this one containing an object
with your AOC session cookie in the `session_id` field. You can get this by inspecting
the headers in your web browser.
"""

import json
import requests
from pkg_resources import resource_stream


class _AOCRetriever:
    user_agent: str
    session_id: str

    def __init__(self) -> None:
        with resource_stream(__name__, ".config.json") as fp:
            config = json.load(fp)

        self.user_agent = config.get("user_agent", "AOC Python Client")
        self.session_id = config["session_id"]

    def get_input(self, day: int) -> str:
        resp = requests.get(
            f"https://adventofcode.com/2023/day/{day}/input",
            cookies={"session": self.session_id},
            headers={"User-Agent": self.user_agent},
        )

        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise ConnectionError(f"HTTP {resp.status_code}: {resp.text}")

        return resp.text


_retriever = _AOCRetriever()


def get_input(day: int) -> str:
    return _retriever.get_input(day=day)
