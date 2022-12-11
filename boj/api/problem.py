import requests

from boj.problem import Problem


def search_problem(problem_id: int) -> dict:
    """
    ID로 문제 가져오기
    :param problem_id: 문제 ID
    :return: Problem Object
    """
    url = "https://solved.ac/api/v3/problem/show"
    params = {"problemId": problem_id}
    headers = {"Content-Type": "application/json"}

    response = requests.get(url=url, params=params, headers=headers)
    response.raise_for_status()

    return Problem.load_json(json=response.json())
