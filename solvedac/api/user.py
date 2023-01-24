import requests

from solvedac.error import UserNotExistError
from solvedac.error import UserApiError


def show_user(user_id: str):
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
            return response.json()
        case 404:
            raise UserNotExistError(
                f"User ID '{user_id}' does not exist"
            )
        case _:
            raise UserApiError(
                f"unexpected error: status code: {status_code}"
            )


def show_user_solved_problem(user_id: str, page: int):
    """
    ID로 유저가 푼 문제 정보 가져오기
    :param user_id: 유저 ID
    :param page: 페이지 번호
    :return: 유저가 푼 문제 정보
    """
    url = "https://solved.ac/api/v3/search/problem"
    params = {"query": f"solved_by:{user_id}", "page": page}
    headers = {"Content-Type": "application/json"}

    response = requests.get(url=url, params=params, headers=headers)

    status_code = response.status_code
    match status_code:
        case 200:
            return response.json()
        case _:
            raise UserApiError(
                f"unexpected error: status code: {status_code}"
            )
