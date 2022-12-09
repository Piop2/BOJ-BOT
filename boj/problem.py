def get_rank(level: int) -> str:
    rank = {
        0: "Unrated",
        1: "Bronze V",
        2: "Bronze IV",
        3: "Bronze III",
        4: "Bronze II",
        5: "Bronze I",
        6: "Silver V",
        7: "Silver IV",
        8: "Silver III",
        9: "Silver II",
        10: "Silver I",
        11: "Gold V",
        12: "Gold IV",
        13: "Gold III",
        14: "Gold II",
        15: "Gold I",
        16: "Platinum V",
        17: "Platinum IV",
        18: "Platinum III",
        19: "Platinum II",
        20: "Platinum I",
        21: "Diamond V",
        22: "Diamond IV",
        23: "Diamond III",
        24: "Diamond II",
        25: "Diamond I",
        26: "Ruby V",
        27: "Ruby IV",
        28: "Ruby III",
        29: "Ruby II",
        30: "Ruby I",
    }
    return rank[level]


def get_tier_image_url(level: int) -> str:
    return f"https://static.solved.ac/tier_small/{level}.svg"


def get_problem_url(problem_id: int) -> str:
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
        self.problem_id = problem_id
        self.title_ko = title_ko
        self.is_solvable = is_solvable
        self.is_partial = is_partial
        self.accepted_user_count = accepted_user_count
        self.level = level
        self.average_tries = average_tries
        self.ko_shorts = ko_shorts

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

    def get_embed(self):
        return
