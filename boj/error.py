class BOJApiError(Exception):
    class ProblemApiError(Exception):
        class ProblemNotExistError(Exception):
            pass
