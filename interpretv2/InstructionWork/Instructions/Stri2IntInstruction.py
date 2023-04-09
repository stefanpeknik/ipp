from InstructionWork.Instruction import Instruction
from InstructionWork.Context import Context


class Stri2IntInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def execute(self, context: Context) -> Context:
        # TODO: implement the STRI2INT instruction
        raise NotImplementedError("Instruction not implemented yet.")
