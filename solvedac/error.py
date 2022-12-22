class SolvedAcApiError(Exception):
    pass


class ProblemApiError(SolvedAcApiError):
    pass


class ProblemNotExistError(ProblemApiError):
    pass


class UserApiError(SolvedAcApiError):
    pass


class UserNotExistError(UserApiError):
    pass
