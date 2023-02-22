import sys
import errorCodes as err
from variable import Variable
from frameStack import FrameStack
from callStack import CallStack
from dataStack import DataStack
from frame import Frame
from exceptions import *
from typing import List, Dict, Tuple


class Instruction:
    def __init__(self, opcode, *args):
        self._opcode = opcode
        self._args = args
        self._op = {
            'MOVE':        self._move,
            'CREATEFRAME': self._createframe,
            'PUSHFRAME':   self._pushframe,
            'POPFRAME':    self._popframe,
            'DEFVAR':      self._defvar,
            'CALL':        self._call,
            'RETURN':      self._return,
            'PUSHS':       self._pushs,
            'POPS':        self._pops,
            'ADD':         self._add,
            'SUB':         self._sub,
            'MUL':         self._mul,
            'IDIV':        self._idiv,
            'LT':          self._lt,
            'GT':          self._gt,
            'EQ':          self._eq,
            'AND':         self._and,
            'OR':          self._or,
            'NOT':         self._not,
            'INT2CHAR':    self._int2char,
            'STRI2INT':    self._stri2int,
            'READ':        self._read,
            'WRITE':       self._write,
            'CONCAT':      self._concat,
            'GETCHAR':     self._getchar,
            'SETCHAR':     self._setchar,
            'TYPE':        self._type,
            'LABEL':       self._label,
            'JUMP':        self._jump,
            'JUMPIFEQ':    self._jumpifeq,
            'JUMPIFNEQ':   self._jumpifneq,
            'EXIT':        self._exit
        }

    @property
    def opcode(self) -> str:
        return self._opcode

    @property
    def args(self) -> Tuple[Variable]:
        return self._args

    def execute(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return self._op[self._opcode](GF, TF, LF_stack, read_from)

    def isConstant(self, arg) -> bool:
        return arg.type == "string" or arg.type == "int" or arg.type == "bool" or arg.type == "nil"

    def isVar(self, arg) -> bool:
        return arg.type == "var"

    def isLabel(self, arg) -> bool:
        return arg.type == "label"

    def isType(self, arg) -> bool:
        return arg.type == "type"

    def getVarNameAndScope(self, arg) -> Tuple[str]:
        return arg.value.split("@")

    def findVar(self, arg, GF: Frame, TF: Frame, LF_stack: FrameStack) -> Variable:
        scope, name = arg.value.split("@")
        if scope == "GF":
            return self.getVarFromGF(name, GF)
        elif scope == "TF":
            return self.getVarFromTF(name, TF)
        elif scope == "LF":
            return self.getVarFromLF(name, LF_stack)

    def getVarFromGF(self, name, GF) -> Variable:
        return GF.getVar(name)

    def getVarFromTF(self, name, TF) -> Variable:
        if TF.defined:
            return TF.getVar(name)
        else:
            raise FrameNotFoundException("TF not found")

    def getVarFromLF(self, name, LF_stack) -> Variable:
        if LF_stack.is_empty() or not LF_stack.top().defined:
            raise FrameNotFoundException("LF not found")
        else:
            return LF_stack.top().getVar(name)

    def setVarInGF(self, name, GF, type, value) -> None:
        GF.getVar(name).set(type, value)

    def setVarInTF(self, name, TF, type, value) -> None:
        if TF.defined:
            TF.getVar(name).set(type, value)
        else:
            raise FrameNotFoundException("TF not found")

    def setVarInLF(self, name, LF_stack, type, value) -> None:
        if LF_stack.is_empty() or not LF_stack.top().defined:
            raise FrameNotFoundException("LF not found")
        else:
            LF_stack.top().getVar(name).set(type, value)

    def setVar(self, arg, GF, TF, LF_stack, type, value) -> Tuple:
        scope, name = self.getVarNameAndScope(
            arg)
        if scope == "GF":
            self.setVarInGF(name, GF, type, value)
        elif scope == "TF":
            self.setVarInTF(name, TF, type, value)
        elif scope == "LF":
            self.setVarInLF(name, LF_stack, type, value)
        return GF, TF, LF_stack

    def defVar(self, arg, GF, TF, LF_stack) -> Tuple:
        scope, name = self.getVarNameAndScope(arg)
        if scope == "GF":
            GF.addVar(name)
        elif scope == "TF":
            TF.addVar(name)
        elif scope == "LF":
            LF_stack.top().addVar(name)
        return GF, TF, LF_stack

    def _move(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            value = var.value
            type = var.type
        else:
            type, value = self.args[1].split('@')

        GF, TF, LF_stack = self.setVar(
            self._args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _createframe(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int][str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        TF = Frame()
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _pushframe(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        if not TF.defined:
            raise FrameNotFoundException("TF not defined")
        LF_stack.push(TF)
        TF = Frame()
        TF.defined = False
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _popframe(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        TF = LF_stack.pop()
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _defvar(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        # TODO
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _call(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        call_stack.push(ins_num)
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _return(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        ins_num = call_stack.pop()
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _pushs(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        # TODO
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _pops(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _add(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _sub(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _mul(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _idiv(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _lt(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _gt(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _eq(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _and(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _or(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _not(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _int2char(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _stri2int(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _read(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _write(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _concat(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _getchar(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _setchar(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _type(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _label(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _jump(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _jumpifeq(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _jumpifneq(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _exit(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: FrameStack, labels: Dict[str, int], call_stack: CallStack, data_stack: DataStack, read_from: str) -> Tuple:
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack
