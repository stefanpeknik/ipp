from InstructionWork.Instruction import Instruction
from InstructionWork.Context import Context

class MoveInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def execute(self, context: Context) -> Context:
        # TODO: implement the MOVE instruction
        raise NotImplementedError("Instruction not implemented yet.")
