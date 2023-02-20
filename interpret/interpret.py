import argparse
import sys
from lxml import etree

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


def validate_xml(xml_string):
    # definice XSD schématu pro validaci
    schema_string = '''<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
        <xs:element name="program">
            <xs:complexType>
                <xs:sequence>
                    <xs:element name="instruction" maxOccurs="unbounded">
                        <xs:complexType>
                            <xs:simpleContent>
                                <xs:extension base="xs:string">
                                    <xs:attribute name="order" type="xs:int" use="required"/>
                                    <xs:attribute name="opcode" type="xs:string" use="required"/>
                                    <xs:attribute name="type" type="xs:string" use="optional"/>
                                </xs:extension>
                            </xs:simpleContent>
                            <xs:element name="arg1" type="xs:string" minOccurs="0" maxOccurs="1">
                                <xs:complexType>
                                    <xs:simpleContent>
                                        <xs:extension base="xs:string">
                                            <xs:attribute name="type" type="xs:string" use="required"/>
                                        </xs:extension>
                                    </xs:simpleContent>
                                </xs:complexType>
                            </xs:element>
                            <xs:element name="arg2" type="xs:string" minOccurs="0" maxOccurs="1">
                                <xs:complexType>
                                    <xs:simpleContent>
                                        <xs:extension base="xs:string">
                                            <xs:attribute name="type" type="xs:string" use="required"/>
                                        </xs:extension>
                                    </xs:simpleContent>
                                </xs:complexType>
                            </xs:element>
                            <xs:element name="arg3" type="xs:string" minOccurs="0" maxOccurs="1">
                                <xs:complexType>
                                    <xs:simpleContent>
                                        <xs:extension base="xs:string">
                                            <xs:attribute name="type" type="xs:string" use="required"/>
                                        </xs:extension>
                                    </xs:simpleContent>
                                </xs:complexType>
                            </xs:element>
                        </xs:complexType>
                    </xs:element>
                </xs:sequence>
                <xs:attribute name="language" type="xs:string" use="required" />
            </xs:complexType>
        </xs:element>
    </xs:schema>'''

    # vytvoření objektu XML schématu
    xmlschema_doc = etree.fromstring(schema_string.encode('utf-8'))
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
    return xml_doc


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
