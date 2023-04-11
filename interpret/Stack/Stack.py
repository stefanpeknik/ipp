from InstructionWork.Exceptions import EmptyStackException


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            raise EmptyStackException("Cannot pop from empty stack.")

    def is_empty(self) -> bool:
        return len(self.stack) == 0

    def top(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            raise EmptyStackException("Cannot get top of empty stack.")

    def size(self):
        return len(self.stack)
