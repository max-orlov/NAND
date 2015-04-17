__author__ = 'Maxim'
SP = 256


class VMStack:
    def __init__(self):
        self._stack = []

    def push(self, segment):
        # Create Push command
        assembly_command = "@{}".format(SP + len(self._stack) + 1) + "\n"
        assembly_command += "M=D" + "\n"
        print(SP + len(self._stack))
        # Do push
        self._stack.append(segment)

        return assembly_command

    def pop(self):
        # Create Pop command
        assembly_command = "@{}".format(SP + len(self._stack)) + "\n"

        # Do pop
        val = self._stack.pop()

        return assembly_command, val