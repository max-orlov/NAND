__author__ = 'Maxim'
SP = 256


class VMStack:
    def __init__(self):
        self._stack_size = 0

    def push(self):
        """
        By this point D should contain the new value.

        :param segment: The segment of which this came from (mainly needed for const)
        :rtype : str
        :return: A string representation of the push command.
        """
        # Create Push command
        assembly_command = "@{}".format(SP + self._stack_size + 1) + "\n"
        assembly_command += "M=D" + "\n"
        # Do push
        self._stack_size += 1

        return assembly_command

    def pop(self):
        """
        pops up the value only into M.
        :rtype : str, segment
        :return: A string representation of the pop command.
        """
        # Create Pop command
        assembly_command = "@{}".format(SP + self._stack_size) + "\n"

        # Do pop
        self._stack_size -= 1

        return assembly_command