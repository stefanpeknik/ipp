import sys

from ArgParser.ArgParser import ArgParser, MissingArgumentException
from XmlParser.XmlParser import XmlParser
from InstructionWork.InstructionFactory import InstructionFactory

from errorCodes import ErrorCodes as err


class Interpret:
    def err_print(self, *args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    def run(self):

        # parse arguments
        try:
            args = ArgParser.parse()
        except MissingArgumentException as e:
            print(e, file=sys.stderr)
            sys.exit(err.ERR_MISSING_ARGUMENT)

        if args.source_file is None:
            xml = sys.stdin.read()
        else:
            # read from file
            try:
                xml = open(args.source_file, "r").read()
            except FileNotFoundError:
                self.err_print("Source file not found.")
                sys.exit(err.ERR_FILE_NOT_FOUND)
        if args.input_file is None:
            input = sys.stdin
        else:
            try:
                input = open(args.input_file, "r")
            except FileNotFoundError:
                self.err_print("Input file not found.")
                sys.exit(err.ERR_FILE_NOT_FOUND)

        # parse XML
        root = XmlParser.parse_xml(xml)

        # store instructions
        instructions_dict = {}  # key: order number, value: instruction
        for instruction in root:
            arg1, arg2, arg3 = None
            for arg in instruction:
                if arg.tag == "arg1":
                    arg1 = arg.text
                elif arg.tag == "arg2":
                    arg2 = arg.text
                elif arg.tag == "arg3":
                    arg3 = arg.text
            args = [arg1, arg2, arg3]  # list of arguments
            instructions_dict[instruction.attrib["order"]] = InstructionFactory().create_instruction(
                instruction.attrib["opcode"], args)  # creates Instruction object and adds it to dictionary
        instructions = [instructions_dict[key] for key in sorted(
            instructions_dict.keys())]  # sorts instructions by order and returns them as a list


if __name__ == '__main__':
    Interpret.run()
