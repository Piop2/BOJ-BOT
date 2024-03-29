import json

from utils.logger import get_logger

user_data_log = get_logger("user_data")

DATA_PATH = "data/user.json"
DATA_BACK_PATH = "data/user.json.back"


class UserData:

    _data: dict

    def __init__(self):
        self.load_data()

    def __iter__(self):
        return self._data.items()

    def __getitem__(self, user_id: str):
        if user_id not in self:
            return False
        else:
            return self._data[user_id]

    def __setitem__(self, user_id: str, value):
        self._data[user_id] = value
        self.save_file()

    def __delitem__(self, user_id: str):
        del self._data[user_id]
        self.save_file()

    def __contains__(self, user_id: int):
        return user_id in self._data

    def keys(self):
        return self._data.keys()

    def load_data(self):
        try:
            with open(DATA_PATH, "r") as f:
                self._data = json.load(f)
        except json.JSONDecodeError:
            self.use_backup_file()

    def save_file(self):
        with open(DATA_PATH, "w") as f:
            json.dump(self._data, f, indent=4)

    def update_user(self, user_id: int, solved_id: str = None, latest_tier: str = None, solved: list = None):
        if solved_id is not None:
            self._data[str(user_id)]["solvedAcId"] = solved_id
        if latest_tier is not None:
            self._data[str(user_id)]["latest_tier"] = latest_tier
        if solved is not None:
            self._data[str(user_id)]["solved"] = solved
        self.save_file()

    def use_backup_file(self):
        user_data_log.warning('loading data failed. using backup file')
        with open(DATA_BACK_PATH, "r") as f:
            self._data = json.load(f)
        self.save_file()

    async def save_backup_file(self):
        try:
            with open(DATA_PATH, "r") as f:
                json.load(f)
        except json.JSONDecodeError:
            return
        with open(DATA_BACK_PATH, "w") as f:
            json.dump(self._data, f, indent=4)
        user_data_log.info('saved backup file')
