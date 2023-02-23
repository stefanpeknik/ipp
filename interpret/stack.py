import sys
import errorCodes as err
from exceptions import *


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()

    def is_empty(self):
        return len(self.stack) == 0

    def top(self):
        if not self.is_empty():
            return self.stack[-1]

    def size(self):
        return len(self.stack)
