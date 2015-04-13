__author__ = 'maxorlov'


class Parser:
    """
    Handles the parsing of a single .vm file, and encapsulates access to the input code. It reads VM commands, parses
    them, and provides convenient access to their components. In addition, it removes all white space and comments.
    """
    def __init__(self, input_stream):
        """
        Opens the input file/stream and gets ready to parse it.

        :param input_stream: specifies the input stream (or file).
        :return: None
        """
        self._in_stream = open(input_stream)
        pass

    def has_more_command(self):
        """
        Are there more commands in the input?

        :rtype: bool
        :return:
        """
        pass

    def advance(self):
        """
        Reads the next command from the input and makes it the current command.
        Should be called only if hasMoreCommands() is true. Initially there is no current command.
        :return: None
        """
        pass

    def command_type(self):
        """
        Returns the type of the current VM command. C_ARITHMETIC is returned for all the arithmetic commands.

        :return: C_ARITHMETIC, C_PUSH, C_POP, C_LABEL, C_GOTO, C_IF, C_FUNCTION, C_RETURN, C_CALL
        """
        pass

    def arg1(self):
        """
        Returns the first argument of the current command. In the case of C_ARITHMETIC,
        the command itself (add, sub, etc.) is returned. Should not be called if the current command is C_RETURN.

        :rtype: str
        :return:
        """
        pass

    def arg2(self):
        """
        Returns the second argument of the current command. Should be called only if the current command is
        C_PUSH, C_POP, C_FUNCTION, or C_CALL.

        :rtype: int
        :return:
        """
        pass
