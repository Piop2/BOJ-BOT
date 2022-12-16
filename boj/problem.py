from boj.utils.rank import get_rank


def _get_problem_url(problem_id: int) -> str:
    return f"https://www.acmicpc.net/problem/{problem_id}"


class Problem:
    def __init__(
        self,
        problem_id: int,
        title_ko: str,
        is_solvable: bool,
        is_partial: bool,
        accepted_user_count: int,
        level: int,
        average_tries: int,
        ko_shorts: list[str, ...],
    ):
        self.id = problem_id
        self.title = title_ko
        self.is_solvable = is_solvable
        self.is_partial = is_partial
        self.accepted_user_count = accepted_user_count
        self.level = level
        self.average_tries = average_tries
        self.shorts = ko_shorts

    @classmethod
    def load_json(cls, json: dict):
        problem_id = json["problemId"]
        title_ko = json["titleKo"]
        is_solvable = json["isSolvable"]
        is_partial = json["isPartial"]
        accepted_user_count = json["acceptedUserCount"]
        level = json["level"]
        average_tries = json["averageTries"]

        ko_shorts = []
        for tag in json["tags"]:
            for display_name in tag["displayNames"]:
                if display_name["language"] == "ko":
                    ko_shorts.append(display_name["short"])

        return cls(
            problem_id=problem_id,
            title_ko=title_ko,
            is_solvable=is_solvable,
            is_partial=is_partial,
            accepted_user_count=accepted_user_count,
            level=level,
            average_tries=average_tries,
            ko_shorts=ko_shorts,
        )

    @property
    def rank(self) -> str:
        return get_rank(level=self.level)

    @property
    def url(self) -> str:
        return _get_problem_url(problem_id=self.id)
