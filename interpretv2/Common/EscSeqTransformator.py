import re

class EscSeqTranformator:
    def transform(self, string: str) -> str:
        return re.sub(r'\\(\d{3})', lambda x: chr(int(x.group(1))), string)
            