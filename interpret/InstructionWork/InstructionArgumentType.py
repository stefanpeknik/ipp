from enum import Enum


class InstructionArgumentType(Enum):
    INT = 1,
    BOOL = 2,
    STRING = 3,
    NIL = 4,
    LABEL = 5,
    TYPE = 6,
    VAR = 7
