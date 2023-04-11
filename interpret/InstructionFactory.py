from Instruction import Instruction
from Instructions import *

from Exceptions import InvalidXMLStructureException


class InstructionFactory:
    def __init__(self):
        self._op = {
            'MOVE':        MoveInstruction,
            'CREATEFRAME': CreateFrameInstruction,
            'PUSHFRAME':   PushFrameInstruction,
            'POPFRAME':    PopFrameInstruction,
            'DEFVAR':      DefVarInstruction,
            'CALL':        CallInstruction,
            'RETURN':      ReturnInstruction,
            'PUSHS':       PushsInstruction,
            'POPS':        PopsInstruction,
            'ADD':         AddInstruction,
            'SUB':         SubInstruction,
            'MUL':         MulInstruction,
            'IDIV':        IdivInstruction,
            'LT':          LtInstruction,
            'GT':          GtInstruction,
            'EQ':          EqInstruction,
            'AND':         AndInstruction,
            'OR':          OrInstruction,
            'NOT':         NotInstruction,
            'INT2CHAR':    Int2CharInstruction,
            'STRI2INT':    Stri2IntInstruction,
            'READ':        ReadInstruction,
            'WRITE':       WriteInstruction,
            'CONCAT':      ConcatInstruction,
            'STRLEN':      StrlenInstruction,
            'GETCHAR':     GetcharInstruction,
            'SETCHAR':     SetcharInstruction,
            'TYPE':        TypeInstruction,
            'LABEL':       LabelInstruction,
            'JUMP':        JumpInstruction,
            'JUMPIFEQ':    JumpifeqInstruction,
            'JUMPIFNEQ':   JumpifneqInstruction,
            'EXIT':        ExitInstruction,
            'DPRINT':      DprintInstruction,
            'BREAK':       BreakInstruction
        }

    def create_instruction(self, opcode: str, *args: list) -> Instruction:
        instruction_class = self._op.get(opcode.upper())
        if instruction_class is None:
            raise InvalidXMLStructureException(
                "Unknown instruction opcode: " + opcode)

        return instruction_class(*args)
