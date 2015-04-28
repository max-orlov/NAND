from Parser import Parser
from VMCommand import VMCommandTypes, VMCommandsArithmeticTypes, c_arithmetic_dictionary
from VMSegment import VMSegmentTypes, c_segment_dictionary
from VMStack import VMStack
from os.path import splitext, basename


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
        self._file_name = None

    def set_file_name(self, file_path):
        """
        Informs the code writer that the translation of a new VM file is started.

        :param file_path: the new file name.
        :return: None
        """
        self._parser = Parser(file_path)
        self._file_name = splitext(basename(file_path))[0]
        self.write_init()
        while self._parser.has_more_command():
            self._parser.advance()
            {
                # Simple arithmetic management (ex 07(
                VMCommandTypes.C_ARITHMETIC: lambda: self.write_arithmetic(self._parser.arg1()),
                VMCommandTypes.C_PUSH: lambda: self.write_push_pop(VMCommandTypes.C_PUSH, self._parser.arg1(),
                                                                   self._parser.arg2()),
                VMCommandTypes.C_POP: lambda: self.write_push_pop(VMCommandTypes.C_POP, self._parser.arg1(),
                                                                  self._parser.arg2()),

                # Label management
                VMCommandTypes.C_LABEL: lambda: self.write_label(self._parser.arg1()),
                VMCommandTypes.C_GOTO: lambda: self.write_go_to(self._parser.arg1()),
                VMCommandTypes.C_IF: lambda: self.write_if(self._parser.arg1()),

                # Function management
                VMCommandTypes.C_FUNCTION: lambda: self.write_function(self._parser.arg1(), self._parser.arg2()),
                VMCommandTypes.C_CALL: lambda: self.write_function(self._parser.arg1(), self._parser.arg2()),
                VMCommandTypes.C_RETURN: lambda: self.write_return()

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
        return "\n".join([self._SP_stack.pop(), "D=M", "@15", "M=D",  # 14 <eq,lt,gt> 15
                          self._SP_stack.pop(), "D=M", "@14", "M=D",
                          "@15", "D=D-M", "@13", "M=D",  # 13 = 14-15
                          # Checking they share the same sign

                          "\n".join(
                              [
                                  # If 14 >= 0 and 15 >= 0 than act as normal
                                  "@14", "D=M", "@__prefix_1lt", "D; JLT",
                                  "@15", "D=M", "@__prefix_fin", "D; JGE",
                                  # If 14 > 0 and 15 < 0, then 14>15, so set D=-1 and act normal
                                  "D=1", "@__prefix_check", "0; JMP",

                                  # If 14 < 0 and 15 < 0, than act as normal
                                  "(__prefix_1lt)", "@15", "D=M", "@__prefix_fin", "D; JLT",
                                  # If 14 < 0 and 15 > 0 than 15>14
                                  "D=-1", "@__prefix_check", "0; JMP",

                                  # If (14 >= 0 , 15 >= 0) or (14 <= 0, 15 <= 0) than finalize the process naturally
                                  "(__prefix_fin)", "@13", "D=M"
                              ]
                          ),

                          "\n".join(
                              ["(__prefix_check)", "@__prefix_is", "D; __condition", "@__prefix_not", "0; JMP",
                               "(__prefix_is)", "D=-1", "@__prefix_end", "0; JMP",
                               "(__prefix_not)", "D=0", "(__prefix_end)"
                              ]
                          ),

        ]).replace("_prefix", self._file_name + "_" + str(self._parser.get_id()) + "_" + condition.lower()).replace(
            "__condition", condition)

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
                index if self._is_segment_const(command, segment) else c_segment_dictionary[segment].value) + "\n"
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
            assembly_command += "@{}".format(c_segment_dictionary[segment].value) + "\n"
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
        return command is not VMCommandTypes.C_ARITHMETIC and c_segment_dictionary[segment] is VMSegmentTypes.CONSTANT

    @staticmethod
    def _is_segment_pointed(segment):
        """
        You shouldn't change D because it might be used to store stuff.
        :param segment:
        :return:
        """
        return c_segment_dictionary[segment] in {VMSegmentTypes.TEMP, VMSegmentTypes.STATIC, VMSegmentTypes.POINTER}

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

    def write_init(self):
        self._out_stream.write("//Init")

    def write_label(self, label):
        assembly_command = '(' + str(self._file_name) + "_" + str(self._parser.get_id()) + "_" + label + ')' + '\n'
        self._out_stream.write(assembly_command)

    def write_go_to(self, label):
        assembly_command = '@' + label + '\n'
        assembly_command += '0; JMP' + '\n'
        self._out_stream.write(assembly_command)

    def write_if(self, label):
        assembly_command = self._SP_stack.pop()
        assembly_command += "D=M" + "\n"
        assembly_command += '@' + label + '\n'
        assembly_command += 'D; JNE'
        self._out_stream.write(assembly_command)

    def write_call(self, function_name, num_args):
        pass

    def write_return(self):
        pass

    def write_function(self, function_name, num_locals):
        pass

    def close(self):
        """
        Closes the output file.

        :return:
        """
        self._out_stream.close()
