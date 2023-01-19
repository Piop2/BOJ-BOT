from solvedac.error import *
import solvedac.api

from solvedac.problem import Problem
from solvedac.user import User


def get_problem(problem_id: int) -> Problem:
    return Problem.load_json(json=solvedac.api.problem.show_problem(problem_id=problem_id))


def get_user(user_id: str) -> User:
    return User.load_json(json=solvedac.api.user.show_user(user_id=user_id))


def user_solved(user_id: str, page: int = 1) -> list[Problem, ...]:
    return list(map(Problem.load_json, solvedac.api.user.search_problem(user_id=user_id, page=page)["items"]))
