import argparse
import sys
from lxml import etree
import re

from errorCodes import ErrorCodes as err
from instruction import Instruction
from argument import Argument
from frame import Frame
from stack import Stack
from exceptions import *


def parse_arguments():
    # creates an argument parser
    parser = argparse.ArgumentParser(
        description="This script will work with the following parameters:", add_help=False)
    parser.add_argument("--help", action="help",
                        help="display this help message and exit")
    parser.add_argument("--source", dest="source_file", metavar="file",
                        help="input file with the XML representation of the source code")
    parser.add_argument("--input", dest="input_file", metavar="file",
                        help="file with inputs for the interpretation of the given source code")
    args = parser.parse_args()

    # checks if the parameters are valid
    if args.source_file is None and args.input_file is None:
        print("At least one of the parameters --source or --input must be specified.")
        sys.exit(err.ERR_MISSING_PARAM)

    return args


def validate_xml(xml_string):
    # creates an XML schema
    schema_string = '''
    <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">

    <xs:element name="program">
        <xs:complexType>
        <xs:sequence>
            <xs:element name="instruction" minOccurs="0" maxOccurs="unbounded" type="instructionType" />
        </xs:sequence>
        <xs:attribute name="language" type="xs:string" use="required" />
        <xs:attribute name="name" type="xs:string" use="optional" />
        <xs:attribute name="description" type="xs:string" use="optional" />
        </xs:complexType>
    </xs:element>

    <xs:complexType name="instructionType">
        <xs:sequence>
        <xs:element name="arg1" minOccurs="0" type="argType" />
        <xs:element name="arg2" minOccurs="0" type="argType" />
        <xs:element name="arg3" minOccurs="0" type="argType" />
        </xs:sequence>
        <xs:attribute name="order" type="xs:positiveInteger" use="required" />
        <xs:attribute name="opcode" type="xs:string" use="required" />
    </xs:complexType>

    <xs:complexType name="argType">
        <xs:simpleContent>
        <xs:extension base="xs:string">
            <xs:attribute name="type" use="required">
            <xs:simpleType>
                <xs:restriction base="xs:string">
                <xs:enumeration value="int" />
                <xs:enumeration value="bool" />
                <xs:enumeration value="string" />
                <xs:enumeration value="nil" />
                <xs:enumeration value="label" />
                <xs:enumeration value="type" />
                <xs:enumeration value="var" />
                </xs:restriction>
            </xs:simpleType>
            </xs:attribute>
        </xs:extension>
        </xs:simpleContent>
    </xs:complexType>

    </xs:schema>
    '''

    # create an XML schema object
    xmlschema_doc = etree.fromstring(schema_string.encode('UTF-8'))
    xmlschema = etree.XMLSchema(xmlschema_doc)

    # create an XML document object
    try:
        xml_doc = etree.fromstring(xml_string.encode('utf-8'))
    except etree.XMLSyntaxError:
        raise InvalidXMLFormatException("Invalid XML format.")

    # validate the XML document against the schema
    if not xmlschema.validate(xml_doc):
        raise InvalidXMLStructureException("Invalid XML structure.")

    return xml_doc


def parse_esc_seqs(value):
    if type == "string":
        value = re.sub(r'\\(\d{3})', lambda x: chr(int(x.group(1))), value)
    return value


def parse_xml(filename=sys.stdin):
    # loads the XML file
    if isinstance(filename, str):
        try:
            with open(filename, "r") as file:
                xml_string = file.read()  # reads the file
        except FileNotFoundError:
            sys.exit(err.ERR_FILE_OPEN)  # file not found
    else:
        xml_string = filename.read()  # reads stdin

    xml_doc = validate_xml(xml_string)  # validates the XML file

    dic_instruc = {}  # dictionary of instructions
    for instruc in xml_doc:  # loops through all instructions
        if instruc.attrib["order"] in dic_instruc:
            raise InvalidXMLStructureException(
                "Invalid XML structure: duplicate order number.")
        args = [None] * 3
        for arg in instruc:  # loops through all arguments
            if arg.tag == "arg1":
                index = 0
            elif arg.tag == "arg2":
                index = 1
            elif arg.tag == "arg3":
                index = 2
            value = arg.text
            if arg.attrib["type"] == "string":  # parses escape sequences
                value = re.sub(r'\\(\d{3})', lambda x: chr(
                    int(x.group(1))), value)
            args[index] = Argument(arg.attrib["type"], value)
        for arg in instruc:  # checks if argument numbering is correct
            if arg.tag == "arg2":
                if args[0] is None:
                    raise InvalidXMLStructureException(
                        "Invalid XML structure: arg2 without arg1.")
            elif arg.tag == "arg3":
                if args[0] is None or args[1] is None:
                    raise InvalidXMLStructureException(
                        "Invalid XML structure: arg3 without arg1 or arg2.")
        args = [arg for arg in args if arg is not None]  # removes None values
        dic_instruc[instruc.attrib["order"]] = Instruction(  # creates Instruction object and adds it to dictionary
            instruc.attrib["opcode"], args)

    # sorts instructions by order and returns them as a list
    instructions = [dic_instruc[key] for key in sorted(dic_instruc.keys())]

    return instructions


def Interprate(instructions, read_from):
    GF = Frame()
    GF.defined = True
    TF = Frame()
    LF_stack = Stack()
    labels = {}
    call_stack = Stack()
    data_stack = Stack()
    if read_from is sys.stdin:  # checks if input is stdin
        ExecuteInstructions(GF, TF, LF_stack, labels,
                            call_stack, data_stack, instructions, sys.stdin)
    else:
        try:  # opens the file
            with open(read_from, "r") as file:
                ExecuteInstructions(GF, TF, LF_stack, labels,
                                    call_stack, data_stack, instructions, file)
        except FileNotFoundError:
            print("File not found.", file=sys.stderr)
            sys.exit(err.ERR_FILE_OPEN)


def ExecuteInstructions(GF, TF, LF_stack, labels, call_stack, data_stack, instructions, read_from):
    for ins_num in range(len(instructions)):
        try:
            ins_num, GF, TF, LF_stack, labels, call_stack, data_stack = instructions[ins_num].execute(
                ins_num, GF, TF, LF_stack, labels, call_stack, data_stack, read_from)
        except SemanticException as e:
            print(e, file=sys.stderr)
            sys.exit(err.ERR_SEMANTIC_ERROR)
        except OperandTypeException as e:
            print(e, file=sys.stderr)
            sys.exit(err.ERR_OPERAND_TYPE_ERROR)
        except UndefinedVariableException as e:
            print(e, file=sys.stderr)
            sys.exit(err.ERR_UNDEFINED_VARIABLE)
        except FrameNotFoundException as e:
            print(e, file=sys.stderr)
            sys.exit(err.ERR_FRAME_NOT_FOUND)
        except MissingValueException as e:
            print(e, file=sys.stderr)
            sys.exit(err.ERR_MISSING_VALUE)
        except InvalidOperandValueException as e:
            print(e, file=sys.stderr)
            sys.exit(err.ERR_INVALID_OPERAND_VALUE)
        except StringErrorException as e:
            print(e, file=sys.stderr)
            sys.exit(err.ERR_STRING_ERROR)
        except Exception as e:
            print(e, file=sys.stderr)
            sys.exit(err.ERR_INTERNAL)


def main():
    # parses arguments
    args = parse_arguments()

    # parses XML file
    if args.source_file:
        instructions = parse_xml(args.source_file)
    else:
        instructions = parse_xml()

    # sets the input source
    if args.input_file:
        read_from = args.input_file
    else:
        read_from = sys.stdin

    # interprets the source code
    Interprate(instructions, read_from)


if __name__ == '__main__':
    main()
