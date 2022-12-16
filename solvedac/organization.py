class Organization:
    def __init__(self, org_id: int, name: str, org_type: str, rating: int, user_count: int, vote_count: int, solved_count: int, color: str):
        self.id = org_id
        self.name = name
        self.type = org_type
        self.rating = rating
        self.user_count = user_count
        self.vote_count = vote_count
        self.solved_count = solved_count
        self.color = color

    @classmethod
    def load_json(cls, json: dict):
        org_id = json["organizationId"]
        name = json["name"]
        org_type = json["type"]
        rating = json["rating"]
        user_count = json["userCount"]
        vote_count = json["voteCount"]
        solved_count = json["solvedCount"]
        color = json["color"]
        return cls(
            org_id=org_id,
            name=name,
            org_type=org_type,
            rating=rating,
            user_count=user_count,
            vote_count=vote_count,
            solved_count=solved_count,
            color=color
        )
