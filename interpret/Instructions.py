import sys

from Instruction import Instruction
from Context import Context
from InstructionArgumentType import InstructionArgumentType

from Variable import Variable
from DataType import DataType

from Frame import Frame

from Mapper import Mapper


from Exceptions import *


# constant types in an array for easier validation
CONST_TYPES = [InstructionArgumentType.INT, InstructionArgumentType.NIL,
               InstructionArgumentType.BOOL, InstructionArgumentType.STRING]


class AddInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 3:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[2].argument_type not in CONST_TYPES and self.args[2].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get left operand
        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame_left, name_left = self.args[1].argument_value.split("@")
            var_left = context.get_var_from_frame(frame_left, name_left)
            if var_left.type != DataType.int:
                raise OperandTypeException("Left operand must be of type int.")
            value_left = var_left.value
        else:
            if self.args[1].argument_type != InstructionArgumentType.INT:
                raise OperandTypeException("Left operand must be of type int.")
            value_left = self.args[1].argument_value

        # get right operand
        if self.args[2].argument_type == InstructionArgumentType.VAR:
            frame_right, name_right = self.args[2].argument_value.split("@")
            var_right = context.get_var_from_frame(frame_right, name_right)
            if var_right.type != DataType.int:
                raise OperandTypeException(
                    "Right operand must be of type int.")
            value_right = var_right.value
        else:
            if self.args[2].argument_type != InstructionArgumentType.INT:
                raise OperandTypeException(
                    "Right operand must be of type int.")
            value_right = self.args[2].argument_value

        # get result variable
        frame_result, name_result = self.args[0].argument_value.split("@")
        var_result = context.get_var_from_frame(frame_result, name_result)

        # set result variable
        var_result.type = DataType.int
        var_result.value = value_left + value_right

        return context


class AndInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 3:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[2].argument_type not in CONST_TYPES and self.args[2].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get left operand
        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame_left, name_left = self.args[1].argument_value.split("@")
            var_left = context.get_var_from_frame(frame_left, name_left)
            if var_left.type != DataType.bool:
                raise OperandTypeException(
                    "Left operand must be of type bool.")
            value_left = var_left.value
        else:
            if self.args[1].argument_type != InstructionArgumentType.BOOL:
                raise OperandTypeException(
                    "Left operand must be of type bool.")
            value_left = self.args[1].argument_value

        # get right operand
        if self.args[2].argument_type == InstructionArgumentType.VAR:
            frame_right, name_right = self.args[2].argument_value.split("@")
            var_right = context.get_var_from_frame(frame_right, name_right)
            if var_right.type != DataType.bool:
                raise OperandTypeException(
                    "Right operand must be of type bool.")
            value_right = var_right.value
        else:
            if self.args[2].argument_type != InstructionArgumentType.BOOL:
                raise OperandTypeException(
                    "Right operand must be of type bool.")
            value_right = self.args[2].argument_value

        # get result variable
        frame_result, name_result = self.args[0].argument_value.split("@")
        var_result = context.get_var_from_frame(frame_result, name_result)

        # set result variable
        var_result.type = DataType.bool
        var_result.value = value_left and value_right

        return context


class BreakInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 0:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()
        print("BREAK:", file=sys.stderr)
        print("Position in ordered instructions: {}".format(
            context.order), file=sys.stderr)
        print("Labels: {}".format(
            [(name, order) for name, order in context.labels.items()]), file=sys.stderr)
        print("Call stack: {}".format(
            [order for order in context.call_stack.stack]), file=sys.stderr)
        print("Data stack: {}".format(
            [(type, val) for type, val in context.data_stack.stack]), file=sys.stderr)
        print("Global frame: {}".format(
            [(name, var.type, var.value) for name, var in context.GF.get_locals()]), file=sys.stderr)
        if context.TF is not None:
            print("Temporary frame: {}".format(
                [(name, var.type, var.value) for name, var in context.TF.get_locals()]), file=sys.stderr)  # type: ignore
        else:
            print("Temporary frame: Not defined now", file=sys.stderr)
        if context.LF_stack.is_empty():
            print("Local frame stack: Empty", file=sys.stderr)
        else:
            for frame_i in range(len(context.LF_stack.stack)):
                print("Local frame {}: {}".format(frame_i, [
                    (name, var.type, var.value) for name, var in context.LF_stack.stack[frame_i].get_locals()]), file=sys.stderr)
        print("--------------------------------------------------", file=sys.stderr)

        return context


class CallInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 1:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.LABEL:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()
        jump_to_order = context.labels.get(self.args[0].argument_value)
        if jump_to_order is None:  # label not found
            raise SemanticException(
                "Label {0} not found.".format(self.args[0].argument_value))
        # push current order to call stack
        context.call_stack.push(context.order)
        context.order = jump_to_order  # jump to label
        return context


class ConcatInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 3:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[2].argument_type not in CONST_TYPES and self.args[2].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get left operand
        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame_left, name_left = self.args[1].argument_value.split("@")
            var_left = context.get_var_from_frame(frame_left, name_left)
            if var_left.type != DataType.string:
                raise OperandTypeException(
                    "Left operand must be of type string.")
            value_left = var_left.value
        else:
            if self.args[1].argument_type != InstructionArgumentType.STRING:
                raise OperandTypeException(
                    "Left operand must be of type string.")
            value_left = self.args[1].argument_value

        # get right operand
        if self.args[2].argument_type == InstructionArgumentType.VAR:
            frame_right, name_right = self.args[2].argument_value.split("@")
            var_right = context.get_var_from_frame(frame_right, name_right)
            if var_right.type != DataType.string:
                raise OperandTypeException(
                    "Right operand must be of type string.")
            value_right = var_right.value
        else:
            if self.args[2].argument_type != InstructionArgumentType.STRING:
                raise OperandTypeException(
                    "Right operand must be of type string.")
            value_right = self.args[2].argument_value

        # get result variable
        frame_result, name_result = self.args[0].argument_value.split("@")
        var_result = context.get_var_from_frame(frame_result, name_result)

        # set result variable
        var_result.type = DataType.string
        var_result.value = value_left + value_right

        return context


class CreateFrameInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 0:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()
        context.TF = Frame()  # type: ignore # create new TF
        return context


class DefVarInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 1:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()
        frame, name = self.args[0].argument_value.split('@')
        var = Variable(name)
        context.insert_var_to_frame(frame, var)
        return context


class DprintInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 1:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type not in CONST_TYPES and self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        if self.args[0].argument_type == InstructionArgumentType.VAR:
            frame, name = self.args[0].argument_value.split('@')
            var = context.get_var_from_frame(frame, name)
            type = var.type
            value = var.value
        else:
            type = Mapper.map_instrucArgType_to_dataType(
                self.args[0].argument_type)
            value = self.args[0].argument_value

        if type == DataType.nil:
            print("nil", file=sys.stderr)
        elif type == DataType.bool:
            if value:
                print("true", file=sys.stderr)
            else:
                print("false", file=sys.stderr)
        elif type == DataType.int:
            print(value, file=sys.stderr)
        elif type == DataType.string:
            print(value, file=sys.stderr)

        return context


class EqInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 3:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[2].argument_type not in CONST_TYPES and self.args[2].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get left operand
        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame_left, name_left = self.args[1].argument_value.split("@")
            var_left = context.get_var_from_frame(frame_left, name_left)
            type_left = var_left.type
            value_left = var_left.value
        else:
            type_left = Mapper.map_instrucArgType_to_dataType(
                self.args[1].argument_type)
            value_left = self.args[1].argument_value

        # get right operand
        if self.args[2].argument_type == InstructionArgumentType.VAR:
            frame_right, name_right = self.args[2].argument_value.split("@")
            var_right = context.get_var_from_frame(frame_right, name_right)
            type_right = var_right.type
            value_right = var_right.value
        else:
            type_right = Mapper.map_instrucArgType_to_dataType(
                self.args[2].argument_type)
            value_right = self.args[2].argument_value

        # check for operand types (nil on either side is ok)
        if type_left != type_right and type_left != DataType.nil and type_right != DataType.nil:
            raise OperandTypeException(
                "Operands must be of same type or at least one nil.")

        # get result variable
        frame_result, name_result = self.args[0].argument_value.split("@")
        var_result = context.get_var_from_frame(frame_result, name_result)

        # set result variable (accept nil as well)
        var_result.type = DataType.bool
        if type_left == DataType.nil and type_right == DataType.nil:  # both nil -> true
            var_result.value = True
        elif type_left == DataType.nil or type_right == DataType.nil:  # one nil -> false
            var_result.value = False
        elif value_left == value_right:  # both not nil and equal -> true
            var_result.value = True
        else:  # both not nil and not equal -> false
            var_result.value = False

        return context


class ExitInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 1:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type not in CONST_TYPES and self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()
        if self.args[0].argument_type == InstructionArgumentType.VAR:
            frame, name = self.args[0].argument_value.split('@')
            var = context.get_var_from_frame(frame, name)
            type = var.type
            exit_code = var.value
        else:
            type = Mapper.map_instrucArgType_to_dataType(
                self.args[0].argument_type)
            exit_code = self.args[0].argument_value

        # check for operand type
        if type != DataType.int:
            raise OperandTypeException(
                "Operand must be of type int.")

        if exit_code < 0 or exit_code > 49:
            raise InvalidOperandValueException(
                "Exit code must be in range 0-49, {0} given.".format(exit_code))
        sys.exit(exit_code)
        return context


class GetcharInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 3:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[2].argument_type not in CONST_TYPES and self.args[2].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get string operand
        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame_string, name_string = self.args[1].argument_value.split("@")
            var_string = context.get_var_from_frame(frame_string, name_string)
            if var_string.type != DataType.string:
                raise OperandTypeException(
                    "Left operand must be of type string.")
            value_string = var_string.value
        else:
            if self.args[1].argument_type != InstructionArgumentType.STRING:
                raise OperandTypeException(
                    "Left operand must be of type string.")
            value_string = self.args[1].argument_value

        # get index operand
        if self.args[2].argument_type == InstructionArgumentType.VAR:
            frame_index, name_index = self.args[2].argument_value.split("@")
            var_index = context.get_var_from_frame(frame_index, name_index)
            if var_index.type != DataType.int:
                raise OperandTypeException(
                    "Right operand must be of type int.")
            value_index = var_index.value
        else:
            if self.args[2].argument_type != InstructionArgumentType.INT:
                raise OperandTypeException(
                    "Right operand must be of type int.")
            value_index = self.args[2].argument_value

        # check if index is in range
        if value_index < 0 or value_index >= len(value_string):
            raise StringErrorException(
                "Index out of range.")

        # get result variable
        frame_result, name_result = self.args[0].argument_value.split("@")
        var_result = context.get_var_from_frame(frame_result, name_result)

        # set result variable
        var_result.type = DataType.string
        var_result.value = value_string[value_index]

        return context


class GtInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 3:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[2].argument_type not in CONST_TYPES and self.args[2].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get left operand
        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame_left, name_left = self.args[1].argument_value.split("@")
            var_left = context.get_var_from_frame(frame_left, name_left)
            type_left = var_left.type
            value_left = var_left.value
        else:
            type_left = Mapper.map_instrucArgType_to_dataType(
                self.args[1].argument_type)
            value_left = self.args[1].argument_value

        # get right operand
        if self.args[2].argument_type == InstructionArgumentType.VAR:
            frame_right, name_right = self.args[2].argument_value.split("@")
            var_right = context.get_var_from_frame(frame_right, name_right)
            type_right = var_right.type
            value_right = var_right.value
        else:
            type_right = Mapper.map_instrucArgType_to_dataType(
                self.args[2].argument_type)
            value_right = self.args[2].argument_value

        # check for operand types
        if type_left != type_right:
            raise OperandTypeException(
                "Operands must be of same type.")
        if type_left == DataType.nil or type_right == DataType.nil:
            raise OperandTypeException("Operands cannot be of type nil.")

        # get result variable
        frame_result, name_result = self.args[0].argument_value.split("@")
        var_result = context.get_var_from_frame(frame_result, name_result)

        # set result variable
        var_result.type = DataType.bool
        if value_left > value_right:
            var_result.value = True
        else:
            var_result.value = False

        return context


class IdivInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 3:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[2].argument_type not in CONST_TYPES and self.args[2].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get left operand
        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame_left, name_left = self.args[1].argument_value.split("@")
            var_left = context.get_var_from_frame(frame_left, name_left)
            if var_left.type != DataType.int:
                raise OperandTypeException("Left operand must be of type int.")
            value_left = var_left.value
        else:
            if self.args[1].argument_type != InstructionArgumentType.INT:
                raise OperandTypeException("Left operand must be of type int.")
            value_left = self.args[1].argument_value

        # get right operand
        if self.args[2].argument_type == InstructionArgumentType.VAR:
            frame_right, name_right = self.args[2].argument_value.split("@")
            var_right = context.get_var_from_frame(frame_right, name_right)
            if var_right.type != DataType.int:
                raise OperandTypeException(
                    "Right operand must be of type int.")
            value_right = var_right.value
        else:
            if self.args[2].argument_type != InstructionArgumentType.INT:
                raise OperandTypeException(
                    "Right operand must be of type int.")
            value_right = self.args[2].argument_value

        # check for division by zero
        if value_right == 0:
            raise InvalidOperandValueException("Division by zero.")

        # get result variable
        frame_result, name_result = self.args[0].argument_value.split("@")
        var_result = context.get_var_from_frame(frame_result, name_result)

        # set result variable
        var_result.type = DataType.int
        var_result.value = value_left // value_right

        return context


class Int2CharInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 2:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get operand
        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame_int, name_int = self.args[1].argument_value.split("@")
            var_int = context.get_var_from_frame(frame_int, name_int)
            if var_int.type != DataType.int:
                raise OperandTypeException(
                    "Left operand must be of type int.")
            value_int = var_int.value
        else:
            if self.args[1].argument_type != InstructionArgumentType.INT:
                raise OperandTypeException(
                    "Left operand must be of type int.")
            value_int = self.args[1].argument_value

        # get result variable
        frame_result, name_result = self.args[0].argument_value.split("@")
        var_result = context.get_var_from_frame(frame_result, name_result)

        # set result variable
        var_result.type = DataType.string
        try:
            var_result.value = chr(value_int)
        except ValueError:
            raise StringErrorException(
                "Invalid value of operand.")

        return context


class JumpInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 1:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.LABEL:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get label
        label = self.args[0].argument_value

        # find where to jump
        where_to_jump = context.labels.get(label)
        if where_to_jump is None:
            raise SemanticException("Label {} not found.".format(label))

        # update context order
        context.order = where_to_jump

        return context


class JumpifeqInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 3:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.LABEL:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[2].argument_type not in CONST_TYPES and self.args[2].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get label
        label = self.args[0].argument_value

        # find where to jump
        where_to_jump = context.labels.get(label)
        if where_to_jump is None:
            raise SemanticException("Label {} not found.".format(label))

        # decide whether to jump

        # get left operand
        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame_left, name_left = self.args[1].argument_value.split("@")
            var_left = context.get_var_from_frame(frame_left, name_left)
            type_left = var_left.type
            value_left = var_left.value
        else:
            type_left = Mapper.map_instrucArgType_to_dataType(
                self.args[1].argument_type)
            value_left = self.args[1].argument_value

        # get right operand
        if self.args[2].argument_type == InstructionArgumentType.VAR:
            frame_right, name_right = self.args[2].argument_value.split("@")
            var_right = context.get_var_from_frame(frame_right, name_right)
            type_right = var_right.type
            value_right = var_right.value
        else:
            type_right = Mapper.map_instrucArgType_to_dataType(
                self.args[2].argument_type)
            value_right = self.args[2].argument_value

        # check for operand types (nil on either side is ok)
        if type_left != type_right and type_left != DataType.nil and type_right != DataType.nil:
            raise OperandTypeException(
                "Operands must be of same type or at least one nil.")

        # decision
        if type_left == DataType.nil and type_right == DataType.nil:  # both nil -> true
            whether_to_jump = True
        elif type_left == DataType.nil or type_right == DataType.nil:  # one nil -> false
            whether_to_jump = False
        elif value_left == value_right:  # both not nil and equal -> true
            whether_to_jump = True
        else:  # both not nil and not equal -> false
            whether_to_jump = False

        # jump if true
        if whether_to_jump:
            context.order = where_to_jump

        return context


class JumpifneqInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 3:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.LABEL:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[2].argument_type not in CONST_TYPES and self.args[2].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get label
        label = self.args[0].argument_value

        # find where to jump
        where_to_jump = context.labels.get(label)
        if where_to_jump is None:
            raise SemanticException("Label {} not found.".format(label))

        # decide whether to jump

        # get left operand
        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame_left, name_left = self.args[1].argument_value.split("@")
            var_left = context.get_var_from_frame(frame_left, name_left)
            type_left = var_left.type
            value_left = var_left.value
        else:
            type_left = Mapper.map_instrucArgType_to_dataType(
                self.args[1].argument_type)
            value_left = self.args[1].argument_value

        # get right operand
        if self.args[2].argument_type == InstructionArgumentType.VAR:
            frame_right, name_right = self.args[2].argument_value.split("@")
            var_right = context.get_var_from_frame(frame_right, name_right)
            type_right = var_right.type
            value_right = var_right.value
        else:
            type_right = Mapper.map_instrucArgType_to_dataType(
                self.args[2].argument_type)
            value_right = self.args[2].argument_value

        # check for operand types (nil on either side is ok)
        if type_left != type_right and type_left != DataType.nil and type_right != DataType.nil:
            raise OperandTypeException(
                "Operands must be of same type or at least one nil.")

        # decision
        if type_left == DataType.nil and type_right == DataType.nil:  # both nil -> false
            whether_to_jump = False
        elif type_left == DataType.nil or type_right == DataType.nil:  # one nil -> true
            whether_to_jump = True
        elif value_left == value_right:  # both not nil and equal -> false
            whether_to_jump = False
        else:  # both not nil and not equal -> true
            whether_to_jump = True

        # jump if true
        if whether_to_jump:
            context.order = where_to_jump

        return context


class LabelInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 1:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

        if self.args[0].argument_type != InstructionArgumentType.LABEL:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # if label not in labels dict, add it and set its start pos to label's order
        if self.args[0].argument_value not in context.labels:
            context.labels[self.args[0].argument_value] = context.order
        else:  # if label is already defined raise exception
            raise SemanticException(
                "Label {} already defined.".format(self.args[0]))

        return context


class LtInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 3:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[2].argument_type not in CONST_TYPES and self.args[2].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get left operand
        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame_left, name_left = self.args[1].argument_value.split("@")
            var_left = context.get_var_from_frame(frame_left, name_left)
            type_left = var_left.type
            value_left = var_left.value
        else:
            type_left = Mapper.map_instrucArgType_to_dataType(
                self.args[1].argument_type)
            value_left = self.args[1].argument_value

        # get right operand
        if self.args[2].argument_type == InstructionArgumentType.VAR:
            frame_right, name_right = self.args[2].argument_value.split("@")
            var_right = context.get_var_from_frame(frame_right, name_right)
            type_right = var_right.type
            value_right = var_right.value
        else:
            type_right = Mapper.map_instrucArgType_to_dataType(
                self.args[2].argument_type)
            value_right = self.args[2].argument_value

        # check for operand types
        if type_left != type_right:
            raise OperandTypeException(
                "Operands must be of same type.")
        if type_left == DataType.nil or type_right == DataType.nil:
            raise OperandTypeException("Operands cannot be of type nil.")

        # get result variable
        frame_result, name_result = self.args[0].argument_value.split("@")
        var_result = context.get_var_from_frame(frame_result, name_result)

        # set result variable
        var_result.type = DataType.bool
        if value_left < value_right:
            var_result.value = True
        else:
            var_result.value = False

        return context


class MoveInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 2:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        frame, name = self.args[0].argument_value.split('@')

        var_move_into = context.get_var_from_frame(frame, name)

        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame, name = self.args[1].argument_value.split('@')
            var_moving = context.get_var_from_frame(frame, name)
            var_move_into.type = var_moving.type
            var_move_into.value = var_moving.value
        else:
            var_move_into.type = Mapper.map_instrucArgType_to_dataType(
                self.args[1].argument_type)
            var_move_into.value = self.args[1].argument_value

        return context


class MulInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 3:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[2].argument_type not in CONST_TYPES and self.args[2].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get left operand
        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame_left, name_left = self.args[1].argument_value.split("@")
            var_left = context.get_var_from_frame(frame_left, name_left)
            if var_left.type != DataType.int:
                raise OperandTypeException("Left operand must be of type int.")
            value_left = var_left.value
        else:
            if self.args[1].argument_type != InstructionArgumentType.INT:
                raise OperandTypeException("Left operand must be of type int.")
            value_left = self.args[1].argument_value

        # get right operand
        if self.args[2].argument_type == InstructionArgumentType.VAR:
            frame_right, name_right = self.args[2].argument_value.split("@")
            var_right = context.get_var_from_frame(frame_right, name_right)
            if var_right.type != DataType.int:
                raise OperandTypeException(
                    "Right operand must be of type int.")
            value_right = var_right.value
        else:
            if self.args[2].argument_type != InstructionArgumentType.INT:
                raise OperandTypeException(
                    "Right operand must be of type int.")
            value_right = self.args[2].argument_value

        # get result variable
        frame_result, name_result = self.args[0].argument_value.split("@")
        var_result = context.get_var_from_frame(frame_result, name_result)

        # set result variable
        var_result.type = DataType.int
        var_result.value = value_left * value_right

        return context


class NotInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 2:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get operand
        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame_to_not, name_to_not = self.args[1].argument_value.split("@")
            var_to_not = context.get_var_from_frame(frame_to_not, name_to_not)
            if var_to_not.type != DataType.bool:
                raise OperandTypeException(
                    "Left operand must be of type bool.")
            value_to_not = var_to_not.value
        else:
            if self.args[1].argument_type != InstructionArgumentType.BOOL:
                raise OperandTypeException(
                    "Left operand must be of type bool.")
            value_to_not = self.args[1].argument_value

        # get result variable
        frame_result, name_result = self.args[0].argument_value.split("@")
        var_result = context.get_var_from_frame(frame_result, name_result)

        # set result variable
        var_result.type = DataType.bool
        var_result.value = not value_to_not

        return context


class OrInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 3:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[2].argument_type not in CONST_TYPES and self.args[2].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get left operand
        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame_left, name_left = self.args[1].argument_value.split("@")
            var_left = context.get_var_from_frame(frame_left, name_left)
            if var_left.type != DataType.bool:
                raise OperandTypeException(
                    "Left operand must be of type bool.")
            value_left = var_left.value
        else:
            if self.args[1].argument_type != InstructionArgumentType.BOOL:
                raise OperandTypeException(
                    "Left operand must be of type bool.")
            value_left = self.args[1].argument_value

        # get right operand
        if self.args[2].argument_type == InstructionArgumentType.VAR:
            frame_right, name_right = self.args[2].argument_value.split("@")
            var_right = context.get_var_from_frame(frame_right, name_right)
            if var_right.type != DataType.bool:
                raise OperandTypeException(
                    "Right operand must be of type bool.")
            value_right = var_right.value
        else:
            if self.args[2].argument_type != InstructionArgumentType.BOOL:
                raise OperandTypeException(
                    "Right operand must be of type bool.")
            value_right = self.args[2].argument_value

        # get result variable
        frame_result, name_result = self.args[0].argument_value.split("@")
        var_result = context.get_var_from_frame(frame_result, name_result)

        # set result variable
        var_result.type = DataType.bool
        var_result.value = value_left or value_right

        return context


class PopFrameInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 0:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()
        if context.LF_stack.is_empty():  # if LF stack is empty raise exception
            raise FrameNotFoundException(
                "LF stack is empty, cannot pop frame from it.")
        context.TF = context.LF_stack.pop()  # pop frame from LF stack
        return context


class PopsInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 1:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        if context.data_stack.is_empty():  # if data stack is empty raise exception
            raise MissingValueException(
                "Data stack is empty, cannot pop from it.")

        # pop tuple (type, value) from data stack
        popped_type, popped_value = context.data_stack.pop()

        # result variable
        frame, name = self.args[0].argument_value.split("@")
        var = context.get_var_from_frame(frame, name)
        var.type = popped_type
        var.value = popped_value

        return context


class PushFrameInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 0:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        if context.TF is None:  # if TF is None raise exception
            raise FrameNotFoundException(
                "TF is None, cannot push it to LF stack.")

        context.LF_stack.push(context.TF)  # push TF to LF stack
        context.TF = None  # set TF to None
        return context


class PushsInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 1:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type not in CONST_TYPES and self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()
        if self.args[0].argument_type == InstructionArgumentType.VAR:  # if argument is variable
            frame, name = self.args[0].argument_value.split('@')
            var = context.get_var_from_frame(
                frame, name)  # get variable from frame
            type = var.type
            value = var.value
        else:  # if argument is constant
            type = Mapper.map_instrucArgType_to_dataType(  # get type of constant
                self.args[0].argument_type)
            value = self.args[0].argument_value  # get value of constant

        # push constant to data stack as tuple (type, value)
        context.data_stack.push((type, value))

        return context


class ReadInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 2:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type != InstructionArgumentType.TYPE:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get type operand
        type = self.args[1].argument_value  # argument already dataType
        if type == DataType.nil:
            raise OperandTypeException(
                "Type operand cannot be nil.")

        # get result variable
        frame_result, name_result = self.args[0].argument_value.split("@")
        var_result = context.get_var_from_frame(frame_result, name_result)

        var_result.type = type  # set type of result variable
        var_result.inited = True  # set result variable to inited

        # read input from context.input
        input = context.input.readline()

        # check if input was not fully read
        if input == "":
            # input was fully read, set result variable to nil
            var_result.type = DataType.nil
            var_result.value = None
        else:  # input was not fully read
            if input[-1] == '\n':
                input = input[:-1]  # remove trailing \n
            if var_result.type == DataType.int:
                # validate that input is int
                try:
                    var_result.value = int(input, 0)
                except ValueError:
                    var_result.type = DataType.nil
                    var_result.value = None
            elif var_result.type == DataType.string:
                var_result.value = input
            elif var_result.type == DataType.bool:
                if input.lower() == "true":
                    var_result.value = True
                else:
                    var_result.value = False
            else:  # nil type not allowed
                raise InvalidOperandValueException(
                    "Type operand cannot be nil.")

        return context


class ReturnInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 0:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()
        if context.call_stack.is_empty():  # if call stack is empty raise exception
            raise MissingValueException(
                "Call stack is empty, cannot pop from it.")
        # pop from call stack and set order to popped value
        context.order = context.call_stack.pop()
        return context


class SetcharInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 3:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[2].argument_type not in CONST_TYPES and self.args[2].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get string operand
        frame_result, name_result = self.args[0].argument_value.split("@")
        var_result = context.get_var_from_frame(frame_result, name_result)
        if var_result.type != DataType.string:
            raise OperandTypeException(
                "First argument must be string.")

        # get index operand
        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame_index, name_index = self.args[1].argument_value.split("@")
            var_index = context.get_var_from_frame(
                frame_index, name_index)
            if var_index.type != DataType.int:
                raise OperandTypeException(
                    "Second argument must be int.")
            index = var_index.value
        else:
            if self.args[1].argument_type != InstructionArgumentType.INT:
                raise OperandTypeException(
                    "Second argument must be int.")
            index = self.args[1].argument_value

        # get char operand
        if self.args[2].argument_type == InstructionArgumentType.VAR:
            frame_char, name_char = self.args[2].argument_value.split("@")
            var_char = context.get_var_from_frame(
                frame_char, name_char)
            if var_char.type != DataType.string:
                raise OperandTypeException(
                    "Third argument must be string.")
            char = var_char.value
        else:
            if self.args[2].argument_type != InstructionArgumentType.STRING:
                raise OperandTypeException(
                    "Third argument must be string.")
            char = self.args[2].argument_value

        # check if index is out of bounds
        if index < 0 or index >= len(var_result.value):
            raise StringErrorException(
                "Index out of bounds.")

        # check if char is not empty
        if char == "":
            raise StringErrorException(
                "Char cannot be empty.")

        # set char at index
        var_result.value = var_result.value[:index] + \
            char[0] + var_result.value[index + 1:]

        return context


class Stri2IntInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 3:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[2].argument_type not in CONST_TYPES and self.args[2].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get string operand
        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame_string, name_string = self.args[1].argument_value.split("@")
            var_string = context.get_var_from_frame(frame_string, name_string)
            if var_string.type != DataType.string:
                raise OperandTypeException(
                    "Left operand must be of type string.")
            value_string = var_string.value
        else:
            if self.args[1].argument_type != InstructionArgumentType.STRING:
                raise OperandTypeException(
                    "Left operand must be of type string.")
            value_string = self.args[1].argument_value

        # get index operand
        if self.args[2].argument_type == InstructionArgumentType.VAR:
            frame_index, name_index = self.args[2].argument_value.split("@")
            var_index = context.get_var_from_frame(frame_index, name_index)
            if var_index.type != DataType.int:
                raise OperandTypeException(
                    "Right operand must be of type int.")
            value_index = var_index.value
        else:
            if self.args[2].argument_type != InstructionArgumentType.INT:
                raise OperandTypeException(
                    "Right operand must be of type int.")
            value_index = self.args[2].argument_value

        # check if index is in range
        if value_index < 0 or value_index >= len(value_string):
            raise StringErrorException(
                "Index out of range.")

        # get result variable
        frame_result, name_result = self.args[0].argument_value.split("@")
        var_result = context.get_var_from_frame(frame_result, name_result)

        # set result variable
        var_result.type = DataType.int
        var_result.value = ord(value_string[value_index])

        return context


class StrlenInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 2:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get string operand
        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame_string, name_string = self.args[1].argument_value.split("@")
            var_string = context.get_var_from_frame(frame_string, name_string)
            if var_string.type != DataType.string:
                raise OperandTypeException(
                    "Left operand must be of type int.")
            value_string = var_string.value
        else:
            if self.args[1].argument_type != InstructionArgumentType.STRING:
                raise OperandTypeException(
                    "Left operand must be of type int.")
            value_string = self.args[1].argument_value

        # get result variable
        frame_result, name_result = self.args[0].argument_value.split("@")
        var_result = context.get_var_from_frame(frame_result, name_result)

        # set result variable
        var_result.type = DataType.int
        var_result.value = len(value_string)

        return context


class SubInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 3:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[2].argument_type not in CONST_TYPES and self.args[2].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get left operand
        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame_left, name_left = self.args[1].argument_value.split("@")
            var_left = context.get_var_from_frame(frame_left, name_left)
            if var_left.type != DataType.int:
                raise OperandTypeException("Left operand must be of type int.")
            value_left = var_left.value
        else:
            if self.args[1].argument_type != InstructionArgumentType.INT:
                raise OperandTypeException("Left operand must be of type int.")
            value_left = self.args[1].argument_value

        # get right operand
        if self.args[2].argument_type == InstructionArgumentType.VAR:
            frame_right, name_right = self.args[2].argument_value.split("@")
            var_right = context.get_var_from_frame(frame_right, name_right)
            if var_right.type != DataType.int:
                raise OperandTypeException(
                    "Right operand must be of type int.")
            value_right = var_right.value
        else:
            if self.args[2].argument_type != InstructionArgumentType.INT:
                raise OperandTypeException(
                    "Right operand must be of type int.")
            value_right = self.args[2].argument_value

        # get result variable
        frame_result, name_result = self.args[0].argument_value.split("@")
        var_result = context.get_var_from_frame(frame_result, name_result)

        # set result variable
        var_result.type = DataType.int
        var_result.value = value_left - value_right

        return context


class TypeInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 2:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[1].argument_type not in CONST_TYPES and self.args[1].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        # get result variable
        frame_result, name_result = self.args[0].argument_value.split("@")
        var_result = context.get_var_from_frame(frame_result, name_result)

        # get symb type and set result variable
        if self.args[1].argument_type == InstructionArgumentType.VAR:
            frame_symb, name_symb = self.args[1].argument_value.split("@")
            var_symb = context.get_var_from_frame(frame_symb, name_symb)
            if var_symb.inited:  # if var is inited set result variable to type of symb
                var_result.value = Mapper.map_dataType_to_string(
                    var_symb.type)
            else:  # if var is not inited set result variable to empty string
                var_result.value = ""
        else:  # if symb is not var set result variable to type of symb
            var_result.value = Mapper.map_dataType_to_string(
                Mapper.map_instrucArgType_to_dataType(self.args[1].argument_type))

        var_result.type = DataType.string
        return context


class WriteInstruction(Instruction):
    def __init__(self, args: list):
        self.args = args

    def validate_args(self):
        if len(self.args) != 1:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")
        if self.args[0].argument_type not in CONST_TYPES and self.args[0].argument_type != InstructionArgumentType.VAR:
            raise InvalidXMLStructureException(
                "Error in instruction arguments.")

    def execute(self, context: Context) -> Context:
        self.validate_args()

        if self.args[0].argument_type == InstructionArgumentType.VAR:
            frame, name = self.args[0].argument_value.split('@')
            var = context.get_var_from_frame(frame, name)
            type = var.type
            value = var.value
        else:
            type = Mapper.map_instrucArgType_to_dataType(
                self.args[0].argument_type)
            value = self.args[0].argument_value

        if type == DataType.nil:
            print("", end="")
        elif type == DataType.bool:
            if value == True:
                print("true", end="")
            else:
                print("false", end="")
        else:
            print(value, end="")

        return context
