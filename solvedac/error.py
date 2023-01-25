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


class ClassApiError(SolvedAcApiError):
    pass


class ClassNotExistError(ClassApiError):
    pass


class TierApiError(SolvedAcApiError):
    pass


class TierNotExistError(TierApiError):
    pass


class SuggestionsApiError(SolvedAcApiError):
    pass
