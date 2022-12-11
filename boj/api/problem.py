import requests

from boj.problem import Problem
from boj.error import BOJApiError


def search_problem(problem_id: int) -> Problem:
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
            return Problem.load_json(json=response.json())
        case 404:
            raise BOJApiError.ProblemApiError.ProblemNotExistError(f"Problem ID '{problem_id}' does not exist")
        case _:
            raise BOJApiError.ProblemApiError(f"unexpected error: status code: {status_code}")
