from Parser import Parser
from VMCommand import VMCommandTypes, VMCommandsArithmeticTypes, c_arithmetic_dictionary
from VMSegment import get_address
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
        self._current_function = "first"

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
                VMCommandTypes.C_CALL: lambda: self.write_call(self._parser.arg1(), self._parser.arg2()),
                VMCommandTypes.C_RETURN: lambda: self.write_return()

            }[self._parser.command_type()]()

    def write_arithmetic(self, command):
        """
        Writes the assembly code that is the translation of the given arithmetic command.

        :param command: translates the command to assembly.
        :return: None
        """
        assembly_commands = {VMCommandsArithmeticTypes.ADD: lambda: self._handle_arithmetic_add(),
                             VMCommandsArithmeticTypes.AND: lambda: self._handle_arithmetic_and(),
                             VMCommandsArithmeticTypes.EQ: lambda: self._handle_arithmetic_eq(),
                             VMCommandsArithmeticTypes.GT: lambda: self._handle_arithmetic_gt(),
                             VMCommandsArithmeticTypes.LT: lambda: self._handle_arithmetic_lt(),
                             VMCommandsArithmeticTypes.NEG: lambda: self._handle_arithmetic_neg(),
                             VMCommandsArithmeticTypes.NOT: lambda: self._handle_arithmetic_not(),
                             VMCommandsArithmeticTypes.OR: lambda: self._handle_arithmetic_or(),
                             VMCommandsArithmeticTypes.SUB: lambda: self._handle_arithmetic_sub()
        }[c_arithmetic_dictionary[command]]()
        assembly_commands.append(self._SP_stack.push())
        self._out_stream.writelines("\n".join(assembly_commands) + "\n")

    def _handle_arithmetic_add(self):
        """
        Creates the 'add' assembly output string
        :return: representation of the 'add' operation assembly string
        """
        return [self._SP_stack.pop(), "D=M", self._SP_stack.pop(), "D=M+D"]

    def _handle_arithmetic_sub(self):
        """
        Creates the 'sub' assembly output string
        :return: representation of the 'sub' operation assembly string
        """
        return [self._SP_stack.pop(), "D=M", self._SP_stack.pop(), "D=M-D"]

    def _handle_arithmetic_neg(self):
        """
        Creates the 'neg' assembly output string
        :return: representation of the 'neg' operation assembly string
        """
        return [self._SP_stack.pop(), "D=M", "D=-D"]

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
        return ["\n".join([self._SP_stack.pop(), "D=M", "@15", "M=D",  # 14 <eq,lt,gt> 15
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
            "__condition", condition) + "\n"]

    def _handle_arithmetic_and(self):
        """
        Creates the 'and' assembly output string
        :return: representation of the 'and' operation assembly string
        """
        return [self._SP_stack.pop(), "D=M", self._SP_stack.pop(), "D=M&D"]

    def _handle_arithmetic_or(self):
        """
        Creates the 'or' assembly output string
        :return: representation of the 'or' operation assembly string
        """
        return [self._SP_stack.pop(), "D=M", self._SP_stack.pop(), "D=M|D"]

    def _handle_arithmetic_not(self):
        """
        Creates the 'not' assembly output string
        :return: representation of the 'not' operation assembly string
        """
        return [self._SP_stack.pop(), "D=!M"]

    def write_push_pop(self, command, segment, index):
        """
        Writes the assembly code that is the translation of the given command, where command is either C_PUSH or C_POP.

        :param command: specifies the command type (push or pop)
        :param segment: the type of the variable (static, argument, local, constant, this/that, pointer, temp)
        :param index: a non negative integer
        :return:
        """
        assembly_commands = []
        if command is VMCommandTypes.C_PUSH:
            # Getting the value specified by the segment and index into M
            assembly_commands.append("@{}".format(
                index if self._is_segment_const(command, segment) else get_address(segment)))
            if self._is_segment_const(command, segment) is False:
                assembly_commands.append(self._find_the_ram_location(segment, index))

            # Pushing the value from M/A into D
            assembly_commands.append("D={}".format("A" if self._is_segment_const(command, segment) else "M"))

            # Pushing the value from D into the stack
            assembly_commands.append(self._SP_stack.push())

        else:  # C_POP
            # Getting the stack top into D
            assembly_commands.append(self._SP_stack.pop())
            assembly_commands.append("D=M")

            # Getting to the specified location into M
            assembly_commands.append("@{}".format(get_address(segment)))
            assembly_commands.append(self._find_the_ram_location(segment, index))

            # Putting the value of D into M
            assembly_commands.append("M=D")

        self._out_stream.writelines("\n".join(assembly_commands) + "\n")

    def _is_segment_const(self, command, segment):
        """
        Determines of the the segment is const or not
        :param command: the command being issued
        :param segment: the segment being addressed
        :return:
        """
        return command is not VMCommandTypes.C_ARITHMETIC and get_address(segment) == get_address("constant")

    @staticmethod
    def _is_segment_pointed(segment):
        """
        You shouldn't change D because it might be used to store stuff.
        :param segment:
        :return:
        """
        return segment in {"temp", "static", "pointer"}

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
        # Setting SP = 256
        assembly_commands = ["\n".join(["@256", "D=A", "@{}".format(get_address("SP")), "M=D"]) + "\n"]
        self._out_stream.writelines(assembly_commands)

        # Calling Sys.init
        self.write_call("Sys.init", 0)
        # TODO: check if only 0 is available for the sys.init function

    def write_label(self, label):
        """
        Writes the assembly code that is the translation of the label command

        :param label: the label name.
        :return:
        """
        assembly_commands = ['(' + str(self._file_name) + "_" + self._current_function + "_" + label + ')']
        self._out_stream.writelines("\n".join(assembly_commands) + "\n")

    def write_go_to(self, label):
        """
        Writes the assembly code that is the translation of the goto command

        :param label: the label name.
        :return:
        """
        assembly_commands = ['@{}_{}_{}'.format(str(self._file_name), self._current_function, label), '0; JMP']
        self._out_stream.writelines("\n".join(assembly_commands) + "\n")

    def write_if(self, label):
        """
        Writes the assembly code that is the translation of the if-goto command

        :param label: the label name.
        :return: None
        """
        assembly_commands = [self._SP_stack.pop(), "D=M", '@{}_{}_{}'.format(str(self._file_name), self._current_function, label), 'D; JNE']
        self._out_stream.writelines("\n".join(assembly_commands) + "\n")

    def write_call(self, function_name, num_args):
        """
        Writes the assembly code that is the translation of the call command.

        :param function_name: function name to call.
        :param num_args: num of args passed to the function.
        :return: None
        """
        assembly_commands = []

        # Pushing the return address label
        assembly_commands.append("@{}".format(function_name + "_return"))
        assembly_commands.append("D=A")
        assembly_commands.append(self._SP_stack.push())

        # Pushing LCL,ARG,THIS,THAT
        segments = ["LCL", "ARG", "THIS", "THAT"]
        for segment in segments:
            assembly_commands.append(
                "\n".join(["@{}".format(get_address(segment)), "D=M", self._SP_stack.push()]))

        # Calculating the value for ARG
        assembly_commands.append("\n".join(
            ["@{}".format(get_address("SP")), "D=M", "@{}".format(num_args), "D=D-A", "@5", "D=D-A"]))

        # Setting the ARG value
        assembly_commands.append("\n".join(["@{}".format(get_address("ARG")), "M=D"]))

        # Calculating the value for LCL
        assembly_commands.append("\n".join(["@{}".format(get_address("SP")), "D=M"]))

        # Setting the LCL value
        assembly_commands.append("\n".join(["@{}".format(get_address("LCL")), "M=D"]))

        # Jumping to function_name
        assembly_commands.append("\n".join(["@{}".format(function_name), "0; JMP"]))

        # Setting the returns-address label
        assembly_commands.append("({})".format(function_name + "_return"))

        self._out_stream.writelines("\n".join(assembly_commands) + "\n")

    def write_return(self):
        """
        Writes the assembly code that is the translation of the return command.

        :return: None
        """
        assembly_commands = []

        # Calculating FRAME
        assembly_commands.append("\n".join(
            ["@{}".format(get_address("LCL")), "D=M", "@{}".format(get_address("R13")),
             "M=D"]))

        # Setting RET (R14)
        assembly_commands.append(
            "\n".join(["@5", "D=D-A", "A=D", "D=M", "@{}".format(get_address("R14")), "M=D"]))

        # We need to save the temporary stack value, than update the sp, and only than update the ARG value (i think)
        # Setting ARG
        assembly_commands.append(
            "\n".join([self._SP_stack.pop(), "D=M", "@{}".format(get_address("ARG")), "M=D"]))

        # Setting SP
        assembly_commands.append("//SETTING SP" + "\n")

        assembly_commands.append(
            "\n".join(["@{}".format(get_address("ARG")), "D=M", "@{}".format(get_address("SP")), "M=D+1"]))

        # Setting THAT
        assembly_commands.append("//SETTING THAT" + "\n")

        assembly_commands.append("\n".join(["@{}".format(get_address("R13")), "D=M-1", "A=D", "D=M",
                                            "@{}".format(get_address("THAT")), "M=D"]))

        # Setting THIS
        assembly_commands.append("//SETTING THIS" + "\n")

        assembly_commands.append(
            "\n".join(["@{}".format(get_address("R13")), "D=M-1", "D=D-1", "A=D", "D=M",
                       "@{}".format(get_address('THIS')), "M=D"]))

        # Setting ARG
        assembly_commands.append("//SETTING ARG" + "\n")
        assembly_commands.append(
            "\n".join(["@{}".format(get_address("R13")), "D=M-1", "D=D-1", "D=D-1", "A=D", "D=M",
                       "@{}".format(get_address("ARG")), "M=D"]))

        # Setting LCL
        assembly_commands.append("//SETTING LCL" + "\n")
        assembly_commands.append(
            "\n".join(
                ["@{}".format(get_address("R13")), "D=M-1", "D=D-1", "D=D-1", "D=D-1", "A=D", "D=M",
                 "@{}".format(get_address("LCL")), "M=D"]))

        # go to RET
        assembly_commands.append("//GOTO RET" + "\n")
        assembly_commands.append("\n".join(["@{}".format(get_address("R14")), "A=M", "0; JMP"]))

        self._out_stream.writelines("\n".join(assembly_commands) + "\n")

    def write_function(self, function_name, num_locals):
        """
        Writes the assembly code that is the translation of the given function command.

        :param function_name: the function name
        :param num_locals: the number of local variables this function has.
        :return: None
        """
        self._current_function = function_name
        assembly_commands = [
            "\n".join(["//NEW FUNCTION : {}".format(function_name), "({})".format(function_name), "D=0"])]
        for _ in range(0, num_locals):
            assembly_commands.append("//PUSHING")
            assembly_commands.append(self._SP_stack.push())
        self._out_stream.writelines("\n".join(assembly_commands) + "\n")

    def close(self):
        """
        Closes the output file.

        :return:
        """
        self._out_stream.close()
