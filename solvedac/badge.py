class Badge:
    def __init__(
        self,
        badge_id: str,
        badge_image_url: str,
        display_name: str,
        display_description: str,
    ):
        self.id = badge_id
        self.image_url = badge_image_url
        self.name = display_name
        self.description = display_description

    @classmethod
    def load_json(cls, json: dict):
        badge_id = json["badgeId"]
        badge_image_url = json["badgeImageUrl"]
        display_name = json["displayName"]
        display_description = json["displayDescription"]
        return cls(
            badge_id=badge_id,
            badge_image_url=badge_image_url,
            display_name=display_name,
            display_description=display_description,
        )
