class SolvedAcApiError(Exception):
    class ProblemApiError(Exception):
        class ProblemNotExistError(Exception):
            pass
    class UserApiError(Exception):
        class UserNotExistError(Exception):
            pass
