import sys
import errorCodes as err
from variable import Variable
from argument import Argument
from stack import Stack
from frame import Frame
from exceptions import *
from typing import List, Dict, Tuple


class Instruction:
    def __init__(self, opcode, args):
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
            'STRLEN':      self._strlen,
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

    def execute(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        return self._op[self._opcode](ins_num, GF, TF, LF_stack, labels, call_stack, data_stack, read_from)

    def isConstant(self, arg: Argument) -> bool:
        return arg.type == "string" or arg.type == "int" or arg.type == "bool" or arg.type == "nil"

    def isVar(self, arg: Argument) -> bool:
        return arg.type == "var"

    def isLabel(self, arg: Argument) -> bool:
        return arg.type == "label"

    def isType(self, arg: Argument) -> bool:
        return arg.type == "type"

    def getVarScopeAndName(self, arg: Argument) -> Tuple[str]:
        return arg.value.split("@")

    def findVar(self, arg: Argument, GF: Frame, TF: Frame, LF_stack: Stack) -> Variable:
        scope, name = arg.value.split("@")
        if scope == "GF":
            return self.getVarFromGF(name, GF)
        elif scope == "TF":
            return self.getVarFromTF(name, TF)
        elif scope == "LF":
            return self.getVarFromLF(name, LF_stack)

    def getVarFromGF(self, name: str, GF: Frame) -> Variable:
        return GF.GetVar(name)

    def getVarFromTF(self, name: str, TF: Frame) -> Variable:
        if TF.defined:
            return TF.GetVar(name)
        else:
            raise FrameNotFoundException("TF not found")

    def getVarFromLF(self, name: str, LF_stack: Stack) -> Variable:
        if LF_stack.is_empty() or not LF_stack.top().defined:
            raise FrameNotFoundException("LF not found")
        else:
            return LF_stack.top().GetVar(name)

    def setVarInGF(self, name: str, GF: Frame, type: str, value) -> None:
        GF.GetVar(name).set(type, value)

    def setVarInTF(self, name: str, TF: Frame, type: str, value) -> None:
        if TF.defined:
            TF.GetVar(name).set(type, value)
        else:
            raise FrameNotFoundException("TF not found")

    def setVarInLF(self, name: str, LF_stack: Stack, type: str, value) -> None:
        if LF_stack.is_empty() or not LF_stack.top().defined:
            raise FrameNotFoundException("LF not found")
        else:
            LF_stack.top().GetVar(name).set(type, value)

    def setVar(self, arg: Argument, GF: Frame, TF: Frame, LF_stack: Stack, type: str, value) -> Tuple:
        scope, name = self.getVarScopeAndName(
            arg)
        if scope == "GF":
            self.setVarInGF(name, GF, type, value)
        elif scope == "TF":
            self.setVarInTF(name, TF, type, value)
        elif scope == "LF":
            self.setVarInLF(name, LF_stack, type, value)
        return GF, TF, LF_stack

    def defVar(self, arg: Argument, GF: Frame, TF: Frame, LF_stack: Stack) -> Tuple:
        scope, name = self.getVarScopeAndName(arg)
        if scope == "GF":
            GF.AddVar(name)
        elif scope == "TF":
            TF.AddVar(name)
        elif scope == "LF":
            LF_stack.top().AddVar(name)
        return GF, TF, LF_stack

    def _move(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            value = var.value
            type = var.type
        else:
            type = self.args[1].type
            value = self.args[1].value

        GF, TF, LF_stack = self.setVar(
            self._args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _createframe(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        TF = Frame()
        TF.defined = True
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _pushframe(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if not TF.defined:
            raise FrameNotFoundException("TF not defined")
        LF_stack.push(TF)
        TF = Frame()
        TF.defined = False
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _popframe(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if LF_stack.is_empty():
            raise FrameNotFoundException("LF not defined")
        TF = LF_stack.pop()
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _defvar(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        try:
            self.findVar(self.args[0], GF, TF, LF_stack)
            raise SemanticException("Variable already defined")
        except UndefinedVariableException:
            pass
        GF, TF, LF_stack = self.defVar(self.args[0], GF, TF, LF_stack)
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _call(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.args[0].value not in labels:
            raise SemanticException("Label not found")
        call_stack.push(ins_num)
        ins_num = labels[self.args[0].value]
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _return(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        ins_num = call_stack.pop()
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _pushs(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[0]):
            var = self.findVar(self.args[0], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            data_stack.push((var.type, var.value))
        else:
            data_stack.push(self.args[0].type, self.args[0].value)
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _pops(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        GF, TF, LF_stack = self.setVar(
            self.args[0], GF, TF, LF_stack, *data_stack.pop())
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _add(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        if self.isVar(self.args[2]):
            var = self.findVar(self.args[2], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            right_type, right_value = var.type, var.value
        else:
            right_type = self.args[2].type
            right_value = self.args[2].value

        if left_type != right_type:
            raise OperandTypeException("Types not matching")

        if left_type == "int":
            type = "int"
            value = str(int(left_value) + int(right_value))
        else:
            raise OperandTypeException(
                "Operation ADD not supported for type " + left_type)

        GF, TF, LF_stack = self.setVar(
            self.args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _sub(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        if self.isVar(self.args[2]):
            var = self.findVar(self.args[2], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            right_type, right_value = var.type, var.value
        else:
            right_type = self.args[2].type
            right_value = self.args[2].value

        if left_type != right_type:
            raise OperandTypeException("Types not matching")

        if left_type == "int":
            type = "int"
            value = str(int(left_value) - int(right_value))
        else:
            raise OperandTypeException(
                "Operation SUB not supported for type " + left_type)

        GF, TF, LF_stack = self.setVar(
            self.args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _mul(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        if self.isVar(self.args[2]):
            var = self.findVar(self.args[2], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            right_type, right_value = var.type, var.value
        else:
            right_type = self.args[2].type
            right_value = self.args[2].value

        if left_type != right_type:
            raise OperandTypeException("Types not matching")

        if left_type == "int":
            type = "int"
            value = str(int(left_value) * int(right_value))
        else:
            raise OperandTypeException(
                "Operation MUL not supported for type " + left_type)

        GF, TF, LF_stack = self.setVar(
            self.args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _idiv(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        if self.isVar(self.args[2]):
            var = self.findVar(self.args[2], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            right_type, right_value = var.type, var.value
        else:
            right_type = self.args[2].type
            right_value = self.args[2].value

        if left_type != right_type:
            raise OperandTypeException("Types not matching")

        if left_type == "int":
            type = "int"
            if int(right_value) == 0:
                raise InvalidOperandValueException("Division by zero")
            value = str(int(left_value) // int(right_value))
        else:
            raise OperandTypeException(
                "Operation IDIV not supported for type " + left_type)

        GF, TF, LF_stack = self.setVar(
            self.args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _lt(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        if self.isVar(self.args[2]):
            var = self.findVar(self.args[2], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            right_type, right_value = var.type, var.value
        else:
            right_type = self.args[2].type
            right_value = self.args[2].value

        if left_type != right_type:
            raise OperandTypeException("Types not matching")

        type = "bool"

        if left_type == "nil":
            raise OperandTypeException(
                "Operation LT not supported for type nil")
        elif left_type == "int":
            value = str(int(left_value) < int(right_value)).lower()
        elif left_type == "bool":
            value = str(bool(left_value) < bool(right_value)).lower()
        elif left_type == "string":
            value = str(left_value < right_value).lower()

        GF, TF, LF_stack = self.setVar(
            self.args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _gt(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        if self.isVar(self.args[2]):
            var = self.findVar(self.args[2], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            right_type, right_value = var.type, var.value
        else:
            right_type = self.args[2].type
            right_value = self.args[2].value

        if left_type != right_type:
            raise OperandTypeException("Types not matching")

        type = "bool"

        if left_type == "nil":
            raise OperandTypeException(
                "Operation GT not supported for type nil")
        elif left_type == "int":
            value = str(int(left_value) > int(right_value)).lower()
        elif left_type == "bool":
            value = str(bool(left_value) > bool(right_value)).lower()
        elif left_type == "string":
            value = str(left_value > right_value).lower()

        GF, TF, LF_stack = self.setVar(
            self.args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _eq(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        if self.isVar(self.args[2]):
            var = self.findVar(self.args[2], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            right_type, right_value = var.type, var.value
        else:
            right_type = self.args[2].type
            right_value = self.args[2].value

        if left_type != "nil" and right_type != "nil" and left_type != right_type:
            raise OperandTypeException("Types not matching")

        type = "bool"

        if left_type == "nil" or right_type == "nil":
            value = str(left_value == "nil" and right_value == "nil").lower()
        elif left_type == "int":
            value = str(int(left_value) == int(right_value)).lower()
        elif left_type == "bool":
            value = str(bool(left_value) == bool(right_value)).lower()
        elif left_type == "string":
            value = str(left_value == right_value).lower()

        GF, TF, LF_stack = self.setVar(
            self.args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _and(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        if self.isVar(self.args[2]):
            var = self.findVar(self.args[2], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            right_type, right_value = var.type, var.value
        else:
            right_type = self.args[2].type
            right_value = self.args[2].value

        if left_type != right_type:
            raise OperandTypeException("Types not matching")

        if left_type == "bool":
            type = "bool"
            value = str(bool(left_value) and bool(right_value))
        else:
            raise OperandTypeException(
                "Operation AND not supported for type " + left_type)

        GF, TF, LF_stack = self.setVar(
            self.args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _or(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        if self.isVar(self.args[2]):
            var = self.findVar(self.args[2], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            right_type, right_value = var.type, var.value
        else:
            right_type = self.args[2].type
            right_value = self.args[2].value

        if left_type != right_type:
            raise OperandTypeException("Types not matching")

        if left_type == "bool":
            type = "bool"
            value = str(bool(left_value) or bool(right_value))
        else:
            raise OperandTypeException(
                "Operation OR not supported for type " + left_type)

        GF, TF, LF_stack = self.setVar(
            self.args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _not(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        if left_type == "bool":
            type = "bool"
            value = not str(bool(left_value))
        else:
            raise OperandTypeException(
                "Operation NOT not supported for type " + left_type)

        GF, TF, LF_stack = self.setVar(
            self.args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _int2char(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        if left_type == "int":
            type = "string"
            try:
                value = chr(left_value)
            except ValueError:
                raise StringErrorException("Invalid ASCII code")
        else:
            raise OperandTypeException(
                "Operation NOT not supported for type " + left_type)

        GF, TF, LF_stack = self.setVar(
            self.args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _stri2int(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        if self.isVar(self.args[2]):
            var = self.findVar(self.args[2], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            right_type, right_value = var.type, var.value
        else:
            right_type = self.args[2].type
            right_value = self.args[2].value

        if left_type != "string" or right_type != "int":
            raise OperandTypeException(
                "Operation STRI2INT not supported for types " + left_type + " and " + right_type)

        if not 0 <= right_value < len(left_value):
            raise StringErrorException("Index out of range")

        type = "int"
        value = str(ord(left_value[right_value]))

        GF, TF, LF_stack = self.setVar(
            self.args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _read(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.args[1].value == "int":
            type = "int"
            try:
                value = str(int(read_from.readline()))
            except ValueError:
                type = "nil"
                value = "nil"
        elif self.args[1].value == "bool":
            type = "bool"
            if read_from.readline().lower() == "true":
                value = "true"
            else:
                value = "false"
        elif self.args[1].value == "string":
            type = "string"
            value = read_from.readline()[:-1]
        else:
            raise InvalidOperandValueException(
                "Invalid type for read: " + self.args[1].value)
        
        GF, TF, LF_stack = self.setVar(
            self.args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _write(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[0]):
            var = self.findVar(self.args[0], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            type = var.type
            value = var.value
        else:
            type = self.args[0].type
            value = self.args[0].value

        if type == "nil":
            print("", end="")
        else:
            print(value, end="")

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _concat(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        if self.isVar(self.args[2]):
            var = self.findVar(self.args[2], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            right_type, right_value = var.type, var.value
        else:
            right_type = self.args[2].type
            right_value = self.args[2].value

        if left_type != right_type:
            raise OperandTypeException("Types not matching")

        if left_type == "string":
            type = "string"
            value = left_value + right_value
        else:
            raise OperandTypeException(
                "Operation CONCAT not supported for type " + left_type)

        GF, TF, LF_stack = self.setVar(
            self.args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _strlen(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        if left_type == "string":
            type = "int"
            value = str(len(left_value))
        else:
            raise OperandTypeException(
                "Operation STRLEN not supported for type " + left_type)

        GF, TF, LF_stack = self.setVar(
            self.args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _getchar(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        if self.isVar(self.args[2]):
            var = self.findVar(self.args[2], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            right_type, right_value = var.type, var.value
        else:
            right_type = self.args[2].type
            right_value = self.args[2].value

        if left_type != "string" or right_type != "int":
            raise OperandTypeException(
                "Operation GETCHAR not supported for types " + left_type + " and " + right_type)

        if not 0 <= right_value < len(left_value):
            raise StringErrorException("Index out of range")

        type = "string"
        value = left_value[right_value]

        GF, TF, LF_stack = self.setVar(
            self.args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _setchar(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        var_to_set = self.findVar(self.args[0], GF, TF, LF_stack)

        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        if self.isVar(self.args[2]):
            var = self.findVar(self.args[2], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            right_type, right_value = var.type, var.value
        else:
            right_type = self.args[2].type
            right_value = self.args[2].value

        if var_to_set.type != "string" or left_type != "int" or right_type != "string":
            raise OperandTypeException("Operation SETCHAR not supported for types " +
                                       var_to_set.type + ", " + left_type + " and " + right_type)

        if not 0 <= left_value < len(var_to_set.value):
            raise StringErrorException("Index out of range")
        if len(right_value) == 0:
            raise StringErrorException("Empty string")

        type = "string"
        index_to_change = left_value
        replacement = right_value[0]
        string_list = list(var_to_set.value)
        string_list[index_to_change] = replacement
        value = "".join(string_list)

        GF, TF, LF_stack = self.setVar(
            self.args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _type(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        type = "string"
        value = left_type

        GF, TF, LF_stack = self.setVar(
            self.args[0], GF, TF, LF_stack, type, value)

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _label(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.args[0].value in labels:
            raise SemanticException("Label already defined")
        labels[self.args[0].value] = ins_num
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _jump(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.args[0].value not in labels:
            raise SemanticException("Label not defined")
        ins_num = labels[self.args[0].value]
        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _jumpifeq(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        if self.isVar(self.args[2]):
            var = self.findVar(self.args[2], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            right_type, right_value = var.type, var.value
        else:
            right_type = self.args[2].type
            right_value = self.args[2].value

        if left_type != "nil" and right_type != "nil" and left_type != right_type:
            raise OperandTypeException("Types not matching")

        type = "bool"

        if left_type == "nil" or right_type == "nil":
            value = str(left_value == "nil" and right_value == "nil").lower()
        elif left_type == "int":
            value = str(int(left_value) == int(right_value)).lower()
        elif left_type == "bool":
            value = str(bool(left_value) == bool(right_value)).lower()
        elif left_type == "string":
            value = str(left_value == right_value).lower()

        if value == "true":
            if self.args[0].value not in labels:
                raise SemanticException("Label not defined")
            ins_num = labels[self.args[0].value]

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _jumpifneq(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        if self.isVar(self.args[2]):
            var = self.findVar(self.args[2], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            right_type, right_value = var.type, var.value
        else:
            right_type = self.args[2].type
            right_value = self.args[2].value

        if left_type != "nil" and right_type != "nil" and left_type != right_type:
            raise OperandTypeException("Types not matching")

        type = "bool"

        if left_type == "nil" or right_type == "nil":
            value = str(left_value == "nil" and right_value == "nil").lower()
        elif left_type == "int":
            value = str(int(left_value) == int(right_value)).lower()
        elif left_type == "bool":
            value = str(bool(left_value) == bool(right_value)).lower()
        elif left_type == "string":
            value = str(left_value == right_value).lower()

        if value == "false":
            if self.args[0].value not in labels:
                raise SemanticException("Label not defined")
            ins_num = labels[self.args[0].value]

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack

    def _exit(self, ins_num: int, GF: Frame, TF: Frame, LF_stack: Stack, labels: Dict[str, int], call_stack: Stack, data_stack: Stack, read_from) -> Tuple:
        if self.isVar(self.args[1]):
            var = self.findVar(self.args[1], GF, TF, LF_stack)
            if not var.inited:
                raise MissingValueException("Variable not inited")
            left_type, left_value = var.type, var.value
        else:
            left_type = self.args[1].type
            left_value = self.args[1].value

        if left_type != "int":
            raise OperandTypeException("Exit code must be int")
        if int(left_value) < 0 or int(left_value) > 49:
            raise InvalidOperandValueException(
                "Exit code must be between 0 and 49")

        if read_from is not sys.stdin:
            read_from.close()

        sys.exit(int(left_value))

        return ins_num, GF, TF, LF_stack, labels, call_stack, data_stack
