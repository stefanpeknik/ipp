from abc import ABCMeta, abstractmethod
from Context import Context


@abstractmethod
class Instruction(metaclass=ABCMeta):
    def __init__(self, args: list):
        self.args = args

    @abstractmethod
    def execute(self, context: Context) -> Context:
        pass
