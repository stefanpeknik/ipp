import sys
import errorCodes as err


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
    def opcode(self):
        return self._opcode

    @property
    def args(self):
        return self._args

    def execute(self, GF, TF, LF_stack, read_from):
        return self._op[self._opcode](GF, TF, LF_stack, read_from)

    def isConstant(self, arg):
        return arg.type == "string" or arg.type == "int" or arg.type == "bool" or arg.type == "nil"

    def isVar(self, arg):
        return arg.type == "var"

    def isLabel(self, arg):
        return arg.type == "label"

    def isType(self, arg):
        return arg.type == "type"

    def getVarScope(self, arg):
        return arg.value.split("@")[0]

    def _move(self, GF, TF, LF_stack, read_from):
        if self.getVarScope(self.args[1]) == "GF":
            pass
        return GF, TF, LF_stack

    def _createframe(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _pushframe(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _popframe(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _defvar(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _call(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _return(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _pushs(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _pops(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _add(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _sub(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _mul(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _idiv(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _lt(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _gt(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _eq(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _and(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _or(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _not(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _int2char(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _stri2int(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _read(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _write(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _concat(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _getchar(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _setchar(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _type(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _label(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _jump(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _jumpifeq(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _jumpifneq(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack

    def _exit(self, GF, TF, LF_stack, read_from):
        return GF, TF, LF_stack
