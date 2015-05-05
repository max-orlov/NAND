

class VMStack:

    def __init__(self):
        pass

    @staticmethod
    def push():
        """
        By this point D should contain the new value.

        :rtype : str
        :return: A string representation of the push command.
        """
        # Pushing the new value
        return "\n".join(["@SP", "A=M", "M=D", "@0", "M=M+1"])

    @staticmethod
    def pop():
        """
        pops up the value only into M.
        :rtype : str, segment
        :return: A string representation of the pop command.
        """
        return "\n".join(["@SP", "M=M-1", "A=M"])

