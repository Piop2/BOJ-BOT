from solvedac.organization import Organization
from solvedac.badge import Badge
from solvedac.background import Background


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
            tier: int,
            rank: int

    ):
        self.name = name
        self.bio = bio
        self.organizations = organizations
        self.badge = badge
        self.background = background
        self.profile_image_url = profile_image_url
        self.solved_count = solved_count
        # self.exp
        self.tier = tier
        # self.rating
        # self.rating_problem_sum
        # self.rating_class
        # self.rating_solved_count
        # self.rating_vote_count
        # self.class_
        # self.class_decoration
        # self.rival_count
        # self.reverse_rival_count
        # self.max_streak
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
        # exp
        tier = json["tier"]
        # rating
        # rating_problem_sum
        # rating_class
        # rating_solved_count
        # rating_vote_count
        # class_
        # class_decoration
        # rival_count
        # reverse_rival_count
        # max_streak
        rank = json["rank"]
        return cls(
            name=name,
            bio=bio,
            organizations=organizations,
            badge=badge,
            background=background,
            profile_image_url=profile_image_url,
            solved_count=solved_count,
            tier=tier,
            rank=rank
        )
