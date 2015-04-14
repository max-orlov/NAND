__author__ = 'maxorlov'
from Parser import Parser
from VMCommandTypes import VMCommandTypes, VMCommandsArithmeticTypes
from VMSegment import VMSegment, VMSegmentTypes, get_segment_type


class CodeWriter:
    """
    Translates VM commands into Hack assembly code.
    """

    def __init__(self, output_stream):
        """
        Opens the output file/stream and gets ready to write into it.

        :param output_stream: output file/stream.
        :return: None
        """
        self._out_stream = open(output_stream, "w")
        self._segments = VMSegment()
        self._parser = None

    def set_file_name(self, file_name):
        """
        Informs the code writer that the translation of a new VM file is started.

        :param file_name: the new file name.
        :return: None
        """
        self._parser = Parser(file_name)
        while self._parser.has_more_command():
            self._parser.advance()
            {
                VMCommandTypes.C_ARITHMETIC: lambda: self.write_arithmetic(self._parser.command_type()),
                VMCommandTypes.C_PUSH: lambda: self.write_push_pop(VMCommandTypes.C_PUSH, self._parser.arg1(),
                                                                   self._parser.arg2()),
                VMCommandTypes.C_POP: lambda: self.write_push_pop(VMCommandTypes.C_POP, self._parser.arg1(),
                                                                  self._parser.arg2()),
            }[self._parser.command_type()]()

    def write_arithmetic(self, command):
        """
        Writes the assembly code that is the translation of the given arithmetic command.

        :param command: translates the command to assembly.
        :return: None
        """
        assembly_command = {
            VMCommandsArithmeticTypes.ADD: lambda: self._handle_arithmetic_add(),
            VMCommandsArithmeticTypes.AND: lambda: self._handle_arithmetic_and(),
            VMCommandsArithmeticTypes.EQ: lambda: self._handle_arithmetic_eq(),
            VMCommandsArithmeticTypes.GT: lambda: self._handle_arithmetic_gt(),
            VMCommandsArithmeticTypes.LT: lambda: self._handle_arithmetic_lt(),
            VMCommandsArithmeticTypes.NEG: lambda: self._handle_arithmetic_neq(),
            VMCommandsArithmeticTypes.NOT: lambda: self._handle_arithmetic_not(),
            VMCommandsArithmeticTypes.OR: lambda: self._handle_arithmetic_or(),
            VMCommandsArithmeticTypes.SUB: lambda: self._handle_arithmetic_sub()
        }[command]()
        self._out_stream.write(assembly_command)

    def _handle_arithmetic_add(self):
        pass

    def _handle_arithmetic_sub(self):
        pass

    def _handle_arithmetic_neq(self):
        pass

    def _handle_arithmetic_eq(self):
        pass

    def _handle_arithmetic_gt(self):
        pass

    def _handle_arithmetic_lt(self):
        pass

    def _handle_arithmetic_and(self):
        pass

    def _handle_arithmetic_or(self):
        pass

    def _handle_arithmetic_not(self):
        pass

    def write_push_pop(self, command, segment, index):
        """
        Writes the assembly code that is the translation of the given command, where command is either C_PUSH or C_POP.

        :param command: specifies the command type (push or pop)
        :param segment: the type of the variable (static, argument, local, constant, this/that, pointer, temp)
        :param index: a non negative integer
        :return:
        """
        if command is VMCommandTypes.C_PUSH:
            self._segments.set_value(segment, index)

        self._out_stream.write(self._segments.get_value(segment, index) + "\n")

    def close(self):
        """
        Closes the output file.

        :return:
        """
        self._out_stream.close()
