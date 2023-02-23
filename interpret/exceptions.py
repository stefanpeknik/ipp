class MissingParamException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class InvalidXMLFormatException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class InvalidXMLStructureException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class SemanticException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class OperandTypeException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class UndefinedVariableException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class FrameNotFoundException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class MissingValueException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class InvalidOperandValueException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class StringErrorException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class InternalErrorException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
