
class UserErrors(Exception):
    def __init__(self, message):
        self.message = message


class UserNotExistError(UserErrors):
    pass

class IncorrectPasswordError(UserErrors):
    pass

class UserAlreadyExist(UserErrors):
    pass

class InvalidEmail(UserErrors):
    pass


