import argparse

from Exceptions import MissingParamException


class ArgParser:
    @staticmethod
    def parse() -> argparse.Namespace:
        # creates an argument parser
        parser = argparse.ArgumentParser(
            description="This script will work with the following parameters:",
            add_help=False  # disable the default --help argument
        )
        # add a custom --help argument
        parser.add_argument("--help", action="store_true",
                            help="display this help message and exit")

        parser.add_argument("--source", dest="source_file", metavar="<file>",
                            help="input file with the XML representation of the source code")
        parser.add_argument("--input", dest="input_file", metavar="<file>",
                            help="file with inputs for the interpretation of the given source code")

        try:  # parse the arguments
            args = parser.parse_args()
        except SystemExit:  # if the arguments are invalid, the parser will try to exit the program, so we catch it
            raise MissingParamException("Invalid arguments.")

        # checks if --help was used together with --source or --input
        if args.help and (args.source_file or args.input_file):
            raise MissingParamException(
                "The --help argument cannot be used together with --source or --input.")

        # check if the --help argument was used
        if args.help:
            print(parser.format_help())
            exit(0)

        # check if the parameters are valid
        if args.source_file is None and args.input_file is None:
            raise MissingParamException(
                "At least one of the parameters --source or --input must be specified.")

        return args
