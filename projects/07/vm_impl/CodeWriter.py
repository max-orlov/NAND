__author__ = 'maxorlov'


class CodeWriter:
    """
    Translates VM commands into Hack assembly code.
    """

    def __init__(self, output_stream):
        """
        Opens the output file/stream and gets ready to write into it.

        :param output: output file/stream.
        :return: None
        """
        self._out_stream = open(output_stream, "w")

    def set_file_name(self, file_name):
        """
        Informs the code writer that the translation of a new VM file is started.

        :param file_name: the new file name.
        :return: None
        """
        pass

    def write_arithmetic(self, command):
        """
        Writes the assembly code that is the translation of the given arithmetic command.

        :param command: translates the command to assembly.
        :return: None
        """
        pass

    def write_push_pop(self, command, segment, index):
        """
        Writes the assembly code that is the translation of the given command, where command is either C_PUSH or C_POP.

        :param command: specifies the command type (push or pop)
        :param segment:
        :param index:
        :return:
        """
        pass

    def close(self):
        """
        Closes the output file.

        :return:
        """
        pass
