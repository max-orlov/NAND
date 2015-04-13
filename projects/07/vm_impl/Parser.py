__author__ = 'maxorlov'
from VMCommands import get_c_command, VMCommands


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
        self._current_line_index = -1
        self._current_command = ''

        self._in_stream = open(input_stream)
        # Creating file iterator with indexes
        self._file_content = [line for index, line in enumerate(self._in_stream)]

    def has_more_command(self):
        """
        Are there more commands in the input?

        :rtype: bool
        :return:
        """
        return self._current_line_index + 1 < len(self._file_content)

    def advance(self):
        """
        Reads the next command from the input and makes it the current command.
        Should be called only if hasMoreCommands() is true. Initially there is no current command.

        :return: None
        """
        if self.has_more_command():
            self._current_line_index += 1
            self._current_command = self._file_content[self._current_line_index]


    def command_type(self):
        """
        Returns the type of the current VM command. C_ARITHMETIC is returned for all the arithmetic commands.

        :return: C_ARITHMETIC, C_PUSH, C_POP, C_LABEL, C_GOTO, C_IF, C_FUNCTION, C_RETURN, C_CALL
        """
        return get_c_command(
            self._current_command.split(' ')[0]) if ' ' in self._current_command else self._current_command.strip()

    def arg1(self):
        """
        Returns the first argument of the current command. In the case of C_ARITHMETIC,
        the command itself (add, sub, etc.) is returned. Should not be called if the current command is C_RETURN.

        :rtype: str
        :return:
        """
        if ' ' in self._current_command:
            command_args = self._current_command.split(' ')
            if self.command_type() == VMCommands.C_ARITHMETIC:
                return command_args[0]
            elif self.command_type() != VMCommands.C_RETURN:
                return command_args[1]
            else:
                return None
        else:
            return None

    def arg2(self):
        """
        Returns the second argument of the current command. Should be called only if the current command is
        C_PUSH, C_POP, C_FUNCTION, or C_CALL.

        :rtype: int
        :return:
        """
        command_args = self._current_command.split(' ')
        if self.command_type() in [VMCommands.C_PUSH, VMCommands.C_POP, VMCommands.C_FUNCTION, VMCommands.C_CALL]:
            return int(command_args[2])
        else:
            return None
