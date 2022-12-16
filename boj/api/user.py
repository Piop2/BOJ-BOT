import requests

from boj.user import User
from boj.error import SolvedAcApiError


def search_user(user_id: str):
    """
    ID로 유저 정보 가져오기
    :param user_id: 유저 ID
    :return: 유저 정보
    """
    url = "https://solved.ac/api/v3/user/show"
    params = {"handle": user_id}
    headers = {"Content-Type": "application/json"}

    response = requests.get(url=url, params=params, headers=headers)

    status_code = response.status_code
    match status_code:
        case 200:
            return User.load_json(response.json())
        case 404:
            raise SolvedAcApiError.UserApiError.UserNotExistError(
                f"User ID '{user_id}' does not exist"
            )
        case _:
            raise SolvedAcApiError.UserApiError(
                f"unexpected error: status code: {status_code}"
            )
