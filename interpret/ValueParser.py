import re

from DataType import DataType
from Mapper import Mapper

from Exceptions import InvalidXMLStructureException


class ValueParser:

    @staticmethod
    def transform_esq_seqs_in_str(string: str) -> str:
        return re.sub(r'\\(\d{3})', lambda x: chr(int(x.group(1))), string)

    @staticmethod
    def parse_int(value: str) -> int:
        try:
            i = int(value, 0)
        except ValueError:
            raise InvalidXMLStructureException("Invalid int value.")
        return i

    @staticmethod
    def parse_bool(value: str) -> bool:
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        else:
            raise InvalidXMLStructureException("Invalid bool value.")

    @staticmethod
    def parse_string(value: str) -> str:
        return ValueParser.transform_esq_seqs_in_str(value)

    @staticmethod
    def parse_nil(value: str) -> None:
        if value != "nil":
            raise InvalidXMLStructureException("Invalid nil value.")
        return None

    @staticmethod
    def parse_label(value: str) -> str:
        if re.match(r'^[a-zA-Z_$&%*!?-][a-zA-Z0-9_$&%*!?-]*$', value) is None:
            raise InvalidXMLStructureException("Invalid label value.")
        return value

    @staticmethod
    def parse_type(value: str) -> DataType:
        if value not in ["int", "bool", "string", "nil"]:
            raise InvalidXMLStructureException("Invalid type value.")
        return Mapper.map_string_to_dataType(value)

    @staticmethod
    def parse_var(value: str) -> str:
        if re.match(r'^(LF|TF|GF)@[a-zA-Z_$&%*!?-][a-zA-Z0-9_$&%*!?-]*$', value) is None:
            raise InvalidXMLStructureException("Invalid var value.")
        return value
