class AlreadyMarkedError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class CantSolveError(Exception):
    def __init__(self, message=None):
        self.message = message
        super().__init__(self.message)
