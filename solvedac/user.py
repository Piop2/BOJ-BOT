from solvedac.organization import Organization
from solvedac.badge import Badge
from solvedac.background import Background


def _get_profile_url(profile_name: str) -> str:
    return f"https://solved.ac/profile/{profile_name}"


class User:
    def __init__(
            self,
            name: str,
            bio: str,
            organizations: list[Organization],
            badge: Badge,
            background: Background,
            profile_image_url: str,
            solved_count: int,
            vote_count: int,
            tier: int,
            rating: int,
            class_: int,
            rival_count: int,
            max_streak: int,
            rank: int

    ):
        self.name = name
        self.bio = bio
        self.organizations = organizations
        self.badge = badge
        self.background = background
        self.image_url = profile_image_url
        self.solved_count = solved_count
        self.vote_count = vote_count
        # self.exp
        self.tier = tier
        self.rating = rating
        # self.rating_problem_sum
        # self.rating_class
        # self.rating_solved_count
        # self.rating_vote_count
        self.class_ = class_
        # self.class_decoration
        self.rival_count = rival_count
        # self.reverse_rival_count
        self.max_streak = max_streak
        self.rank = rank

    @classmethod
    def load_json(cls, json: dict):
        name = json["handle"]
        bio = json["bio"]
        organizations = [Organization.load_json(i) for i in json["organizations"]]
        badge = Badge.load_json(json["badge"])
        background = Background.load_json(json["background"])
        profile_image_url = json["profileImageUrl"]
        solved_count = json["solvedCount"]
        vote_count = json["voteCount"]
        # exp
        tier = json["tier"]
        rating = json["rating"]
        # rating_problem_sum
        # rating_class
        # rating_solved_count
        # rating_vote_count
        class_ = json["class"]
        # class_decoration
        # rival_count
        # reverse_rival_count
        rival_count = json["rivalCount"]
        max_streak = json["maxStreak"]
        rank = json["rank"]
        return cls(
            name=name,
            bio=bio,
            organizations=organizations,
            badge=badge,
            background=background,
            profile_image_url=profile_image_url,
            solved_count=solved_count,
            vote_count=vote_count,
            tier=tier,
            rating=rating,
            class_=class_,
            rival_count=rival_count,
            max_streak=max_streak,
            rank=rank
        )

    @property
    def url(self) -> str:
        return _get_profile_url(profile_name=self.name)
