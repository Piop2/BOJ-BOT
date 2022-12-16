class Background:
    def __init__(self, background_id: str, background_image_url: str, author: str, author_url: str, display_name: str, display_description: str):
        self.id = background_id
        self.image_url = background_image_url
        self.author = author
        self.author_url = author_url
        self.name = display_name
        self.description = display_description

    @classmethod
    def load_json(cls, json: dict):
        background_id = json["backgroundId"]
        background_image_url = json["backgroundImageUrl"]
        author = json["author"]
        author_url = json["authorUrl"]
        display_name = json["displayName"]
        display_description = json["displayDescription"]
        return cls(
            background_id=background_id,
            background_image_url=background_image_url,
            author=author,
            author_url=author_url,
            display_name=display_name,
            display_description=display_description
        )
