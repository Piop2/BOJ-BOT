import json

USER_DATA_PATH = "data/user.json"


def get_user_info(user_id: int) -> dict | bool:
    with open(USER_DATA_PATH, "r") as f:
        user_data = json.load(f)
    try:
        return user_data[str(user_id)]
    except KeyError:
        return False
