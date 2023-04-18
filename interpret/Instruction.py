from abc import ABCMeta, abstractmethod
from Context import Context


@abstractmethod
class Instruction(metaclass=ABCMeta):
    def __init__(self, args: list):
        self.args = args

    @abstractmethod
    def validate_args(self):
        """
        Validates the arguments passed to the instruction.
        Throws an exception if the arguments are invalid.
        """
        pass

    @abstractmethod
    def execute(self, context: Context) -> Context:
        """
        Validates the arguments (if any), then executes the instruction.
        `context` is the current context of the program.
        """
        pass
