import argparse

from Exceptions import MissingParamException


class ArgParser:
    @staticmethod
    def parse() -> argparse.Namespace:
        # creates an argument parser
        parser = argparse.ArgumentParser(
            description="This script will work with the following parameters:", add_help=False)
        parser.add_argument("--help", action="help",
                            help="display this help message and exit")
        parser.add_argument("--source", dest="source_file", metavar="<file>",
                            help="input file with the XML representation of the source code")
        parser.add_argument("--input", dest="input_file", metavar="<file>",
                            help="file with inputs for the interpretation of the given source code")
        args = parser.parse_args()

        # checks if the parameters are valid
        if args.source_file is None and args.input_file is None:
            raise MissingParamException(
                "At least one of the parameters --source or --input must be specified.")

        return args
