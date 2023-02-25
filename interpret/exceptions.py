class MissingParamException(Exception):  # 10
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class InvalidXMLFormatException(Exception):  # 31
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class InvalidXMLStructureException(Exception):  # 32
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class SemanticException(Exception):  # 52
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class OperandTypeException(Exception):  # 53
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class UndefinedVariableException(Exception):  # 54
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class FrameNotFoundException(Exception):  # 55
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class MissingValueException(Exception):  # 56
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class InvalidOperandValueException(Exception):  # 57
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class StringErrorException(Exception):  # 58
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class InternalErrorException(Exception):  # 99
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
