import re


class EscSeqTransformator:
    @staticmethod
    def transform(string: str) -> str:
        return re.sub(r'\\(\d{3})', lambda x: chr(int(x.group(1))), string)
