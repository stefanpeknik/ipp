import argparse
import sys
from lxml import etree

from errorCodes import ErrorCodes as err
from instruction import Instruction
from argument import Argument
from frame import Frame
from frameStack import FrameStack
from callStack import CallStack
from dataStack import DataStack


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


def validate_xml(xml_string):
    # definice XSD schématu pro validaci
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
        <xs:attribute name="order" type="xs:integer" use="required" />
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

    # vytvoření objektu XML schématu
    xmlschema_doc = etree.fromstring(schema_string.encode('UTF-8'))
    xmlschema = etree.XMLSchema(xmlschema_doc)

    # vytvoření objektu XML dokumentu
    try:
        xml_doc = etree.fromstring(xml_string.encode('utf-8'))
    except etree.XMLSyntaxError:
        sys.exit(err.ERR_INVALID_XML_FORMAT)

    # ověření validity XML dokumentu
    if not xmlschema.validate(xml_doc):
        sys.exit(err.ERR_INVALID_XML_STRUCTURE)

    return xml_doc


def parse_xml(filename=sys.stdin):
    if isinstance(filename, str):
        with open(filename, "r") as file:
            xml_string = file.read()
    else:
        xml_string = filename.read()

    xml_doc = validate_xml(xml_string)

    dic_instruc = {}
    for instruc in xml_doc:
        args = [None] * 3
        for arg in instruc:
            if arg.text == "arg1":
                args[0] = Argument(arg.attrib["type"], arg.text)
            elif arg.text == "arg2":
                if args[0] is None:
                    sys.exit(err.ERR_INVALID_XML_STRUCTURE)
                args[1] = Argument(arg.attrib["type"], arg.text)
            elif arg.text == "arg3":
                if args[0] is None or args[1] is None:
                    sys.exit(err.ERR_INVALID_XML_STRUCTURE)
                args[2] = Argument(arg.attrib["type"], arg.text)
        args = [arg for arg in args if arg is not None]
        dic_instruc[instruc.attrib["order"]] = Instruction(
            instruc.attrib["opcode"], args)

    instructions = [dic_instruc[key] for key in sorted(dic_instruc.keys())]

    return instructions


def Interprate(instructions, read_from):
    GF = Frame()
    GF.defined = True
    TF = Frame()
    LF_stack = FrameStack()
    labels = {}
    call_stack = CallStack()
    data_stack = DataStack()

    for ins_num in range(len(instructions)):
        ins_num, GF, TF, LF_stack, labels, call_stack, data_stack = instructions[ins_num].execute(
            ins_num, GF, TF, LF_stack, labels, call_stack, data_stack, read_from)


def main():
    args = parse_arguments()

    if args.source_file:
        instructions = parse_xml(args.source_file)
    else:
        instructions = parse_xml()

    if args.input_file:
        read_from = args.input_file
    else:
        read_from = sys.stdin

    for ins in instructions:
        print(ins.opcode + " : " + ins.args)

    Interprate(instructions, read_from)


if __name__ == '__main__':
    main()
