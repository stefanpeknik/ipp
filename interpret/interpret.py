import argparse
import sys
import xml.etree.ElementTree as ET

from interpret.errorCodes import ErrorCodes as err


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="This script will work with the following parameters:", add_help=False)
    parser.add_argument("--help", action="help",
                        help="display this help message and exit")
    parser.add_argument("--source", dest="source_file", metavar="file",
                        help="input file with the XML representation of the source code")
    parser.add_argument("--input", dest="input_file", metavar="file",
                        help="file with inputs for the interpretation of the given source code")
    args = parser.parse_args()

    if args.source_file is None and args.input_file is None:
        print("At least one of the parameters --source or --input must be specified.")
        sys.exit(err.ERR_MISSING_PARAM)

    return args


def parse_xml_file(filename=sys.stdin):
    if isinstance(filename, str):
        with open(filename, "r") as file:
            xml_data = file.read()
    else:
        xml_data = filename.read()
    try:
        tree = ET.ElementTree(ET.fromstring(xml_data))
    except ET.ParseError:
        print(
            f"Error: File '{filename}' is not well-formed XML.", file=sys.stderr)
        sys.exit(err.ERR_INVALID_XML_FORMAT)
    root = tree.getroot()
    
    for instruc in root:
        
    
    # for instruc in root:
    #     if instruc.tag != 'instruction':
    #         print(
    #             f"Error: Unexpected element '{instruc.tag}' found in XML file.", file=sys.stderr)
    #         sys.exit(err.ERR_INVALID_XML_STRUCTURE)
    #     for i in len(instruc.items()):
    #         foundArg = False
    #         for arg in instruc:
    #             if arg.tag == 'arg' + i:
    #                 foundArg = True
    #                 break
    #         if not foundArg:
    #             print(
    #                 f"Error: Wrongly indexed argument found in XML file under instruction {instruc.tag}.", file=sys.stderr)
    #             sys.exit(err.ERR_INVALID_XML_STRUCTURE)
    return root


def Interprate(xml, read_from):
    pass


def main():
    args = parse_arguments()

    if args.source_file:
        xml = parse_xml_file(args.source_file)
    else:
        xml = parse_xml_file()

    if args.input_file:
        read_from = args.input_file
    else:
        read_from = sys.stdin

    Interprate(xml, read_from)


if __name__ == '__main__':
    main()
