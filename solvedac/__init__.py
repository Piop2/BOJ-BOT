from solvedac.error import *
import solvedac.api

from solvedac.problem import Problem
from solvedac.user import User


def get_problem(problem_id: int) -> Problem:
    return Problem.load_json(json=solvedac.api.problem.show_problem(problem_id=problem_id))


def get_class_problem(class_id: int) -> list[Problem, ...]:
    return list(map(Problem.load_json, solvedac.api.problem.show_class_problem(class_id=class_id)["items"]))


def get_tier_problem(tier_id: int) -> list[Problem, ...]:
    page = solvedac.api.problem.show_tier_problem(tier_id=tier_id, page=1)["count"]//50 + 1
    problems = []
    for i in range(page):
        problems.extend(list(map(Problem.load_json,
                                 solvedac.api.problem.show_tier_problem(tier_id=tier_id, page=i+1)["items"])))
    return problems


def get_user(user_id: str = None) -> User:
    return User.load_json(json=solvedac.api.user.show_user(user_id=user_id))


def get_user_solved(user_id: str) -> list[Problem, ...]:
    page = solvedac.api.user.show_user_solved_problem(user_id=user_id, page=1)["count"]//50 + 1
    problems = []
    for i in range(page):
        problems.extend(list(map(Problem.load_json,
                                 solvedac.api.user.show_user_solved_problem(user_id=user_id, page=i+1)["items"])))
    return problems
