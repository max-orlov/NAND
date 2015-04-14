__author__ = 'Maxim'


class VMStack():
    def __init__(self):
        self._command_stack = []

    def push(self, item):
        return self._command_stack.append(item)

    def pop(self):
        return self._command_stack.pop()
