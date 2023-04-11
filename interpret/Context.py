from Frame import Frame
from Stack import Stack
from typing import TextIO
from Variable import Variable

from Exceptions import FrameNotFoundException, InvalidXMLStructureException


class Context:
    def __init__(self, input: TextIO):
        self.GF = Frame()  # global frame
        self.TF = None  # temporary frame
        self.LF_stack = Stack()  # stack of local frames
        self.call_stack = Stack()  # stack of instruction numbers representing calls
        self.data_stack = Stack()  # stack of values on the data stack
        self.labels = {}  # str -> int (label name -> instruction number)
        self.input = input  # input file
        self.order = 0  # current instruction number

    def insert_var_to_frame(self, frame: str, var: Variable):
        if frame == "GF":
            self.GF.AddVar(var)
        elif frame == "TF":
            if self.TF is None:
                raise FrameNotFoundException("Frame TF not defined.")
            self.TF.AddVar(var)
        elif frame == "LF":
            if self.LF_stack.is_empty():
                raise FrameNotFoundException("Frame LF not defined.")
            self.LF_stack.top().AddVar(var)
        else:
            raise InvalidXMLStructureException("Invalid frame name.")

    def get_var_from_frame(self, frame: str, name: str):
        if frame == "GF":
            return self.GF.GetVarByName(name)
        elif frame == "TF":
            if self.TF is None:
                raise FrameNotFoundException("Frame TF not defined.")
            return self.TF.GetVarByName(name)
        elif frame == "LF":
            if self.LF_stack.is_empty():
                raise FrameNotFoundException("Frame LF not defined.")
            return self.LF_stack.top().GetVarByName(name)
        else:
            raise InvalidXMLStructureException("Invalid frame name.")

    def is_var_in_frame(self, frame: str, name: str):
        if not self.is_frame_defined(frame):
            raise FrameNotFoundException("Frame {} not defined.".format(frame))
        if frame == "GF":
            return self.GF.IsVarInFrame(name)
        elif frame == "TF":
            if self.TF is None:
                raise FrameNotFoundException("Frame TF not defined.")
            return self.TF.IsVarInFrame(name)
        elif frame == "LF":
            if self.LF_stack.is_empty():
                raise FrameNotFoundException("Frame LF not defined.")
            return self.LF_stack.top().IsVarInFrame(name)
        else:
            raise InvalidXMLStructureException("Invalid frame name.")

    def is_frame_defined(self, frame: str):
        if frame == "GF":
            return self.GF is not None
        elif frame == "TF":
            if self.TF is None:
                raise FrameNotFoundException("Frame TF not defined.")
            return self.TF is not None
        elif frame == "LF":
            if self.LF_stack.is_empty():
                raise FrameNotFoundException("Frame LF not defined.")
            return self.LF_stack.top() is not None
        else:
            raise InvalidXMLStructureException("Invalid frame name.")
