__author__ = 'maxorlov'
from Parser import Parser
from VMCommandTypes import VMCommandTypes, VMCommandsArithmeticTypes, c_arithmetic_dictionary
from VMSegment import VMSegmentTypes, get_segment_type
from VMStack import VMStack


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
        self._SP_stack = VMStack()
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
                VMCommandTypes.C_ARITHMETIC: lambda: self.write_arithmetic(self._parser.arg1()),
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
            VMCommandsArithmeticTypes.NEG: lambda: self._handle_arithmetic_neg(),
            VMCommandsArithmeticTypes.NOT: lambda: self._handle_arithmetic_not(),
            VMCommandsArithmeticTypes.OR: lambda: self._handle_arithmetic_or(),
            VMCommandsArithmeticTypes.SUB: lambda: self._handle_arithmetic_sub()
        }[c_arithmetic_dictionary[command]]()
        self._out_stream.write(assembly_command if assembly_command is not None else "")

    def _handle_arithmetic_add(self):
        return "\n".join([self._SP_stack.pop(), "D=M", self._SP_stack.pop(), "D=M+D", self._SP_stack.push()])

    def _handle_arithmetic_sub(self):
        return "\n".join([self._SP_stack.pop(), "D=M", self._SP_stack.pop(), "D=M-D", self._SP_stack.push()])

    def _handle_arithmetic_neg(self):
        return "\n".join([self._SP_stack.pop(), "D=M", "D=-D", self._SP_stack.push()])

    def _handle_arithmetic_eq(self):
        return self._handle_boolean_condition("JEQ")

    def _handle_arithmetic_gt(self):
        return self._handle_boolean_condition("JGT")

    def _handle_arithmetic_lt(self):
        return self._handle_boolean_condition("JLT")

    def _handle_boolean_condition(self, condition):
        return "\n".join([self._SP_stack.pop(), "D=M", self._SP_stack.pop(), "D=M-D",
                          "\n".join(
                              ["@___label_eq", "D; __condition", "@___label_not_eq", "0; JMP", "(___label_eq)", "D=-1",
                               "@___label_end", "0; JMP", "(___label_not_eq)", "D=0", "(___label_end)"]).replace(
                              "__label", str(self._parser.get_id())).replace("__condition", condition),
                          self._SP_stack.push()])

    def _handle_arithmetic_and(self):
        return "\n".join([self._SP_stack.pop(), "D=M", self._SP_stack.pop(), "D=M&D", self._SP_stack.push()])

    def _handle_arithmetic_or(self):
        return "\n".join([self._SP_stack.pop(), "D=M", self._SP_stack.pop(), "D=M|D", self._SP_stack.push()])

    def _handle_arithmetic_not(self):
        return "\n".join([self._SP_stack.pop(), "D=!M", self._SP_stack.push()])

    def write_push_pop(self, command, segment, index):
        """
        Writes the assembly code that is the translation of the given command, where command is either C_PUSH or C_POP.

        :param command: specifies the command type (push or pop)
        :param segment: the type of the variable (static, argument, local, constant, this/that, pointer, temp)
        :param index: a non negative integer
        :return:
        """
        # Does not handle non existing variable yet

        if command is VMCommandTypes.C_PUSH:
            # Parsing
            assembly_command = "\n".join(["@{}".format(self._parser.arg2() if self._is_segment_const() else
                                                       str(get_segment_type(
                                                           self._parser.arg1()).value + self._parser.arg2())),
                                          "D={}".format("A" if self._is_segment_const() else "M"),
                                          self._SP_stack.push()])

        else:  # C_POP case
            assembly_command = "\n".join([self._SP_stack.pop(), "D=M",
                                          "@{}".format(get_segment_type(segment).value + index),
                                          "M=D"])

        self._out_stream.write(assembly_command)

    def _is_segment_const(self):
        return self._parser.command_type() is not VMCommandTypes.C_ARITHMETIC and get_segment_type(
            self._parser.arg1()) is VMSegmentTypes.CONSTANT

    def close(self):
        """
        Closes the output file.

        :return:
        """
        self._out_stream.close()
