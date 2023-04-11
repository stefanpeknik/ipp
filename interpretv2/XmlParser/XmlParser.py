from lxml import etree

from InstructionWork.Exceptions import InvalidXMLFormatException, InvalidXMLStructureException


class XmlParser:

    @staticmethod
    def validate_xml(xml_string: str) -> etree.Element:
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
            <xs:all>
            <xs:element name="arg1" minOccurs="0" maxOccurs="1" type="argType" />
            <xs:element name="arg2" minOccurs="0" maxOccurs="1" type="argType" />
            <xs:element name="arg3" minOccurs="0" maxOccurs="1" type="argType" />
            </xs:all>
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

        order_nums = []  # list of order numbers
        for instruc in xml_doc:  # loops through all instructions
            if instruc.attrib["order"] in order_nums:
                raise InvalidXMLStructureException(
                    "Invalid XML structure: duplicate order number: {0}.".format(instruc.attrib["order"]))
            args = [arg for arg in instruc]
            if "arg2" in [arg.tag for arg in args]:  # checks if arg2 is present
                # checks if arg1 is present as well
                if "arg1" not in [arg.tag for arg in args]:
                    raise InvalidXMLStructureException(
                        "Invalid XML structure: arg2 without arg1.")
            if "arg3" in [arg.tag for arg in args]:  # checks if arg3 is present
                # checks if arg1 and arg2 are present as well
                if "arg1" not in [arg.tag for arg in args] or "arg2" not in [arg.tag for arg in args]:
                    raise InvalidXMLStructureException(
                        "Invalid XML structure: arg3 without arg1 or arg2.")

        return xml_doc

    @staticmethod
    def parse_xml(input: str) -> etree.Element:
        # validates the XML file and returns the root element
        return XmlParser.validate_xml(input)
