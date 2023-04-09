from InstructionWork.Instruction import Instruction
from InstructionWork.Context import Context

class JumpifeqInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def execute(self, context: Context) -> Context:
        # TODO: implement the JUMPIFEQ instruction
        raise NotImplementedError("Instruction not implemented yet.")
