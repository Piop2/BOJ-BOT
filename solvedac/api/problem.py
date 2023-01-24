import requests

from solvedac.error import ProblemNotExistError
from solvedac.error import ProblemApiError
from solvedac.error import ClassNotExistError
from solvedac.error import ClassApiError
from solvedac.error import TierNotExistError
from solvedac.error import TierApiError


def show_problem(problem_id: int):
    """
    ID로 문제 가져오기
    :param problem_id: 문제 ID
    :return: Problem Object
    """
    url = "https://solved.ac/api/v3/problem/show"
    params = {"problemId": problem_id}
    headers = {"Content-Type": "application/json"}

    response = requests.get(url=url, params=params, headers=headers)

    status_code = response.status_code
    match status_code:
        case 200:
            return response.json()
        case 404:
            raise ProblemNotExistError(
                f"Problem ID '{problem_id}' does not exist"
            )
        case _:
            raise ProblemApiError(
                f"unexpected error: status code: {status_code}"
            )


def show_class_problem(class_id: int):
    """
    Class번호로 해당하는 문제 가져오기
    :param class_id: Class 번호
    :return: Problem Object
    """
    url = "https://solved.ac/api/v3/search/problem"
    params = {"query": f"in_class:{class_id}", "page": 1}
    headers = {"Content-Type": "application/json"}

    response = requests.get(url=url, params=params, headers=headers)

    status_code = response.status_code
    match status_code:
        case 200:
            return response.json()
        case 404:
            raise ClassNotExistError(
                f"Class '{class_id}' does not exist"
            )
        case _:
            raise ClassApiError(
                f"unexpected error: status code: {status_code}"
            )


def show_tier_problem(tier_id: int, page: int):
    """
    Tier ID로 문제 가져오기
    :param tier_id: Tier ID
    :param page: 페이지 번호
    :return: Problem Object
    """
    url = "https://solved.ac/api/v3/search/problem"
    params = {"query": f"tier:{tier_id}", "page": page}
    headers = {"Content-Type": "application/json"}

    response = requests.get(url=url, params=params, headers=headers)

    status_code = response.status_code
    match status_code:
        case 200:
            return response.json()
        case 404:
            raise TierNotExistError(
                f"Tier ID '{tier_id}' does not exist"
            )
        case _:
            raise TierApiError(
                f"unexpected error: status code: {status_code}"
            )
