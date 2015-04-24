from VMCommand import c_command_dictionary, VMCommandTypes


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
        self._file_content = []
        for line in self._in_stream.readlines():
            if "//" in line and len(line[:line.index("//")].strip()) != 0:
                self._file_content.append(' '.join(line[:line.index("//")].split()))
            elif "//" not in line and len(line.strip()) > 0:
                self._file_content.append(' '.join(line.split()))

    def get_id(self):
        return self._current_line_index

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
        return c_command_dictionary[
            self._current_command.split(' ')[0] if ' ' in self._current_command else self._current_command.strip()]

    def arg1(self):
        """
        Returns the first argument of the current command. In the case of C_ARITHMETIC,
        the command itself (add, sub, etc.) is returned. Should not be called if the current command is C_RETURN.

        :rtype: str
        :return:
        """
        if self.command_type() == VMCommandTypes.C_ARITHMETIC:
            return self._current_command.split(' ')[0]
        elif self.command_type() != VMCommandTypes.C_RETURN:
            return self._current_command.split(' ')[1]
        else:
            return None

    def arg2(self):
        """
        Returns the second argument of the current command. Should be called only if the current command is
        C_PUSH, C_POP, C_FUNCTION, or C_CALL.

        :rtype: int
        :return:
        """
        if self.command_type() in [VMCommandTypes.C_PUSH, VMCommandTypes.C_POP, VMCommandTypes.C_FUNCTION,
                                   VMCommandTypes.C_CALL]:
            return int(self._current_command.split(' ')[2])
        else:
            return None
