__author__ = 'Maxim'


class VMStack:

    def __init__(self):
        self._sp_index = 0

    def push(self):
        """
        By this point D should contain the new value.

        :rtype : str
        :return: A string representation of the push command.
        """
        # Pushing the new value
        return "\n".join(["@0", "A=M", "M=D", "@0", "M=M+1"]) + "\n"


    def pop(self):
        """
        pops up the value only into M.
        :rtype : str, segment
        :return: A string representation of the pop command.
        """
        return "\n".join(["@0", "M=M-1", "A=M"]) + "\n"

