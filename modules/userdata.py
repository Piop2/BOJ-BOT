import json

from utils.logger import get_logger

user_data_log = get_logger("user_data")


class UserData:

    _data: dict

    def __init__(self):
        self.data_path = "data/user.json"
        self.data_back_path = "data/user.json.back"
        self.load_data()

    def __iter__(self):
        return self._data.items()

    def __getitem__(self, user_id: int):
        if user_id not in self:
            return False
        else:
            return self._data[str(user_id)]

    def __contains__(self, user_id: int):
        return user_id in self._data

    def keys(self):
        return self._data.keys()

    def load_data(self):
        try:
            with open(self.data_path, "r") as f:
                self._data = json.load(f)
        except json.JSONDecodeError:
            self.use_backup_file()

    def save_file(self):
        with open(self.data_path, "w") as f:
            json.dump(self._data, f, indent=4)

    def update_user(self, user_id: int, solved_id: str = None, latest_tier: str = None, solved: list = None):
        if solved_id is not None:
            self._data[str(user_id)]["solved_id"] = solved_id
        if latest_tier is not None:
            self._data[str(user_id)]["latest_tier"] = latest_tier
        if solved is not None:
            self._data[str(user_id)]["solved"] = solved
        self.save_file()

    def use_backup_file(self):
        user_data_log.warning('loading data failed. using backup file')
        with open(self.data_back_path, "r") as f:
            self._data = json.load(f)
        self.save_file()

    async def save_backup_file(self):
        with open(self.data_back_path, "w") as f:
            json.dump(self._data, f, indent=4)
        user_data_log.info('saved backup file')

    def delete_user(self, user_id: int):
        del self._data[str(user_id)]
        self.save_file()
