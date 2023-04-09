from Common.EscSeqTransformator import EscSeqTransformator
from InstructionArgumentType import InstructionArgumentType


class InstructionArgument:
    def __init__(self, argument_type: InstructionArgumentType, argument_value):
        self.argument_type = argument_type

        if argument_type == InstructionArgumentType.STRING:
            self.argument_value = EscSeqTransformator.transform(argument_value)
        else:
            self.argument_value = argument_value
