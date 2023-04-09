from InstructionWork.Instruction import Instruction
from InstructionWork.Context import Context

class LabelInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def execute(self, context: Context) -> Context:
        # TODO: implement the LABEL instruction
        raise NotImplementedError("Instruction not implemented yet.")
