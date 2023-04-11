import sys

from ArgParser.ArgParser import ArgParser
from XmlParser.XmlParser import XmlParser
from InstructionWork.InstructionFactory import InstructionFactory
from InstructionWork.Context import Context
from InstructionWork.InstructionArgument import InstructionArgument
from InstructionWork.Instructions import *

from Common.ErrorHandler import ErrorHandler

from ErrorCodes import ErrorCodes as err


class Interpret:
    def run(self):

        # parse arguments
        try:
            args = ArgParser.parse()

            if args.source_file is None:
                xml = sys.stdin.read()
            else:
                # read from file
                try:
                    xml = open(args.source_file, "r").read()
                except FileNotFoundError as e:
                    raise OpenFileException(
                        "Source file {0} not found.".format(args.source_file)) from e
            if args.input_file is None:
                input = sys.stdin
            else:
                try:
                    input = open(args.input_file, "r")
                except FileNotFoundError as e:
                    raise OpenFileException(
                        "Input file {0} not found.".format(args.input_file)) from e

            # parse XML
            root = XmlParser.parse_xml(xml)

            # store instructions
            instructions_dict = {}  # key: order number, value: instruction
            for instruction in root:
                arg1, arg2, arg3 = None, None, None
                for arg in instruction:
                    if arg.tag == "arg1":
                        arg1 = InstructionArgument(
                            arg.attrib['type'], arg.text)
                    elif arg.tag == "arg2":
                        arg2 = InstructionArgument(
                            arg.attrib['type'], arg.text)
                    elif arg.tag == "arg3":
                        arg3 = InstructionArgument(
                            arg.attrib['type'], arg.text)
                args = [arg1, arg2, arg3]  # list of arguments
                # remove None values
                args = [arg for arg in args if arg is not None]
                order = int(instruction.attrib["order"])
                if order in instructions_dict:
                    raise InvalidXMLStructureException(
                        "Instruction with order number {0} already exists.".format(order))
                instructions_dict[order] = InstructionFactory().create_instruction(
                    instruction.attrib["opcode"].upper(), args)  # creates Instruction object and adds it to dictionary
            instructions = [instruc for _, instruc in sorted(
                instructions_dict.items())]

            # create context
            context = Context(input=input)

            # run interpretting

            # find labels
            for context.order in range(len(instructions)):
                if isinstance(instructions[context.order], LabelInstruction):
                    instructions[context.order].execute(context)

            context.order = 0  # reset order

            # execute instructions
            while context.order < len(instructions):
                # skip already executed labels
                if not isinstance(instructions[context.order], LabelInstruction):
                    context = instructions[context.order].execute(context)
                context.order += 1

        # catch exceptions
        except MissingParamException as e:
            ErrorHandler.err_exit(err.ERR_MISSING_PARAM, e)
        except InvalidXMLFormatException as e:
            ErrorHandler.err_exit(err.ERR_INVALID_XML_FORMAT, e)
        except InvalidXMLStructureException as e:
            ErrorHandler.err_exit(err.ERR_INVALID_XML_STRUCTURE, e)
        except SemanticException as e:
            ErrorHandler.err_exit(err.ERR_SEMANTIC_ERROR, e)
        except OperandTypeException as e:
            ErrorHandler.err_exit(err.ERR_OPERAND_TYPE_ERROR, e)
        except UndefinedVariableException as e:
            ErrorHandler.err_exit(err.ERR_UNDEFINED_VARIABLE, e)
        except FrameNotFoundException as e:
            ErrorHandler.err_exit(err.ERR_FRAME_NOT_FOUND, e)
        except MissingValueException as e:
            ErrorHandler.err_exit(err.ERR_MISSING_VALUE, e)
        except InvalidOperandValueException as e:
            ErrorHandler.err_exit(err.ERR_INVALID_OPERAND_VALUE, e)
        except StringErrorException as e:
            ErrorHandler.err_exit(err.ERR_STRING_ERROR, e)
        except InternalErrorException as e:
            ErrorHandler.err_exit(err.ERR_INTERNAL, e)
        finally:
            if input != sys.stdin:  # close input file if it was opened
                input.close()


if __name__ == '__main__':
    Interpret().run()
