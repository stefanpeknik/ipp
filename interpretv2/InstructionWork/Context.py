from Frame import Frame
from Stack import Stack


class Context:
    def __init__(self) -> None:
        self.GF = Frame()
        self.GF.defined = True
        self.TF = Frame()
        self.LF_stack = Stack()
        self.call_stack = Stack()
        self.data_stack = Stack()
        self.labels = {}  # str -> int (label name -> instruction number)
