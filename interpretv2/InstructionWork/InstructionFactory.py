import Instruction
from Instructions import MoveInstruction, CreateFrameInstruction, PushFrameInstruction, PopFrameInstruction, DefVarInstruction, CallInstruction, ReturnInstruction, PushsInstruction, PopsInstruction, AddInstruction, SubInstruction, MulInstruction, IdivInstruction, LtInstruction, GtInstruction, EqInstruction, AndInstruction, OrInstruction, NotInstruction, Int2CharInstruction, Stri2IntInstruction, ReadInstruction, WriteInstruction, ConcatInstruction, StrlenInstruction, GetcharInstruction, SetcharInstruction, TypeInstruction, LabelInstruction, JumpInstruction, JumpifeqInstruction, JumpifneqInstruction, ExitInstruction


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
            'EXIT':        ExitInstruction
        }

    def create_instruction(self, opcode: str, *args: list):
        # it is expected that the opcode is in the dictionary as it was parser job to check that
        instruction_class = self._op.get(opcode)

        return instruction_class(*args)
