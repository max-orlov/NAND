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
        assembly_command = {VMCommandsArithmeticTypes.ADD: lambda: self._handle_arithmetic_add(),
                            VMCommandsArithmeticTypes.AND: lambda: self._handle_arithmetic_and(),
                            VMCommandsArithmeticTypes.EQ: lambda: self._handle_arithmetic_eq(),
                            VMCommandsArithmeticTypes.GT: lambda: self._handle_arithmetic_gt(),
                            VMCommandsArithmeticTypes.LT: lambda: self._handle_arithmetic_lt(),
                            VMCommandsArithmeticTypes.NEG: lambda: self._handle_arithmetic_neg(),
                            VMCommandsArithmeticTypes.NOT: lambda: self._handle_arithmetic_not(),
                            VMCommandsArithmeticTypes.OR: lambda: self._handle_arithmetic_or(),
                            VMCommandsArithmeticTypes.SUB: lambda: self._handle_arithmetic_sub()
                           }[c_arithmetic_dictionary[command]]() + "\n"
        assembly_command += self._SP_stack.push()
        self._out_stream.write(assembly_command)

    def _handle_arithmetic_add(self):
        """
        Creates the 'add' assembly output string
        :return: representation of the 'add' operation assembly string
        """
        return "\n".join([self._SP_stack.pop(), "D=M", self._SP_stack.pop(), "D=M+D"])

    def _handle_arithmetic_sub(self):
        """
        Creates the 'sub' assembly output string
        :return: representation of the 'sub' operation assembly string
        """
        return "\n".join([self._SP_stack.pop(), "D=M", self._SP_stack.pop(), "D=M-D"])

    def _handle_arithmetic_neg(self):
        """
        Creates the 'neg' assembly output string
        :return: representation of the 'neg' operation assembly string
        """
        return "\n".join([self._SP_stack.pop(), "D=M", "D=-D"])

    def _handle_arithmetic_eq(self):
        """
        Creates the 'eq' assembly output string
        :return: representation of the 'eq' operation assembly string
        """
        return self._handle_boolean_condition("JEQ")

    def _handle_arithmetic_gt(self):
        """
        Creates the 'gt' assembly output string
        :return: representation of the 'gt' operation assembly string
        """
        return self._handle_boolean_condition("JGT")

    def _handle_arithmetic_lt(self):
        """
        Creates the 'lt' assembly output string
        :return: representation of the 'lt' operation assembly string
        """
        return self._handle_boolean_condition("JLT")

    def _handle_boolean_condition(self, condition):
        """
        A helper function to all boolean operations (as they are quite the same)
        :param condition: the type of the condition (eq,gt,lt)
        :return: representation of the given condition operation assembly string
        """
        return "\n".join([self._SP_stack.pop(), "D=M", self._SP_stack.pop(), "D=M-D",
                          "\n".join(
                              ["@___label_eq", "D; __condition", "@___label_not_eq", "0; JMP", "(___label_eq)", "D=-1",
                               "@___label_end", "0; JMP", "(___label_not_eq)", "D=0", "(___label_end)"]).replace(
                              "__label", str(self._parser.get_id())).replace("__condition", condition)])

    def _handle_arithmetic_and(self):
        """
        Creates the 'and' assembly output string
        :return: representation of the 'and' operation assembly string
        """
        return "\n".join([self._SP_stack.pop(), "D=M", self._SP_stack.pop(), "D=M&D"])

    def _handle_arithmetic_or(self):
        """
        Creates the 'or' assembly output string
        :return: representation of the 'or' operation assembly string
        """
        return "\n".join([self._SP_stack.pop(), "D=M", self._SP_stack.pop(), "D=M|D"])

    def _handle_arithmetic_not(self):
        """
        Creates the 'not' assembly output string
        :return: representation of the 'not' operation assembly string
        """
        return "\n".join([self._SP_stack.pop(), "D=!M"])

    def write_push_pop(self, command, segment, index):
        """
        Writes the assembly code that is the translation of the given command, where command is either C_PUSH or C_POP.

        :param command: specifies the command type (push or pop)
        :param segment: the type of the variable (static, argument, local, constant, this/that, pointer, temp)
        :param index: a non negative integer
        :return:
        """
        assembly_command = ""
        if command is VMCommandTypes.C_PUSH:
            # Getting the value specified by the segment and index into M
            assembly_command += "@{}".format(
                index if self._is_segment_const(command, segment) else get_segment_type(segment).value) + "\n"
            if self._is_segment_const(command, segment) is False:
                assembly_command += self._find_the_ram_location(segment, index)

            # Pushing the value from M/A into D
            assembly_command += "D={}".format("A" if self._is_segment_const(command, segment) else "M") + "\n"

            # Pushing the value from D into the stack
            assembly_command += self._SP_stack.push() + "\n"

        else:  # C_POP
            # Getting the stack top into D
            assembly_command += self._SP_stack.pop() + "\n"
            assembly_command += "D=M" + "\n"

            # Getting to the specified location into M
            assembly_command += "@{}".format(get_segment_type(segment).value) + "\n"
            assembly_command += self._find_the_ram_location(segment, index)

            # Putting the value of D into M
            assembly_command += "M=D" + "\n"

        self._out_stream.write(assembly_command)

    @staticmethod
    def _is_segment_const(command, segment):
        """
        Determines of the the segment is const or not
        :param command: the command being issued
        :param segment: the segment being addressed
        :return:
        """
        return command is not VMCommandTypes.C_ARITHMETIC and get_segment_type(segment) is VMSegmentTypes.CONSTANT

    @staticmethod
    def _is_segment_pointed(segment):
        """
        You shouldn't change D because it might be used to store stuff.
        :param segment:
        :return:
        """
        return get_segment_type(segment) in {VMSegmentTypes.TEMP, VMSegmentTypes.STATIC, VMSegmentTypes.POINTER}

    def _find_the_ram_location(self, segment, index):
        """
        Finds the exact location based on segment and index, and puts it into A

        :param segment: the segment
        :param index: the index
        :return:
        """
        assembly_command = ("" if self._is_segment_pointed(segment) else "A=M") + "\n"
        for i in range(0, index):
            assembly_command += "A=A+1" + "\n"
        return assembly_command

    def close(self):
        """
            Closes the output file.

            :return:
            """

        self._out_stream.close()
