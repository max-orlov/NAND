__author__ = 'Maxim'


class VMStack:

    def __init__(self):
        pass

    def push(self):
        """
        By this point D should contain the new value.

        :rtype : str
        :return: A string representation of the push command.
        """
        # Pushing the new value
        assembly_command = "@0" + "\n" + "A=M" + "\n"
        assembly_command += "M=D" + "\n"

        # Updating the SP
        assembly_command += "@0" + "\n" + "M=M+1" + "\n"

        return assembly_command

    def pop(self):
        """
        pops up the value only into M.
        :rtype : str, segment
        :return: A string representation of the pop command.
        """
        # Updating the SP
        assembly_command = "@0" + "\n" + "M=M-1" + "\n"

        # Getting the value
        assembly_command += "A=M" + "\n"

        return assembly_command