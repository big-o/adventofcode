import requests
import os


class _AOCRetriever:
    user_agent: str
    session_id: str

    def __init__(self) -> None:
        self.user_agent = os.getenv("AOC_USER_AGENT") or "AOC Python Client"
        self.session_id = os.getenv("AOC_SESSION_ID")
        assert self.session_id is not None, "AOC_SESSION_ID env variable not set."

    def get_input(self, day: int) -> str:
        resp = requests.get(
            f"https://adventofcode.com/2023/day/{day}/input",
            cookies={"session": self.session_id},
            headers={"User-Agent": self.user_agent},
        )

        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise ConnectionError(f"HTTP {resp.status}: {resp.text}")

        return resp.text


_retriever = _AOCRetriever()


def get_input(day: int) -> str:
    return _retriever.get_input(day=day)
