import sys
from Parser import Parser, CommandType
from SymbolTable import SymbolTable
from Code import jump, dest, comp
from os import listdir, path
from os.path import isfile, join, isdir



def _write_to_file(filename, content):
    out_file_name = filename[: -len(".asm")] + ".hack"
    out_file = open(out_file_name, "w")
    out_file.write(content)
    out_file.close()


class Main:
    def __init__(self):
        """

        """
        self._parser = None
        self._symbol_table = None
        self._current_symbol_num = 16
        self._current_command_num = 0

    def parse_file(self, filename):
        """
        parses a given ASM file into HACK language.
        :param filename: the ASM filename.
        :return:
        """
        self._symbol_table = SymbolTable()

        """first pass."""
        self._parser = Parser(filename)
        while self._parser.has_more_commands():
            self._parser.advance()
            is_l_type = self._parser.command_type() != CommandType.L_COMMAND
            self._current_command_num += is_l_type or (not is_l_type and not self._parser.is_label())
            if self._parser.command_type() == CommandType.L_COMMAND and self._parser.is_label():
                    self._symbol_table.addEntry(self._parser.symbol(), self._current_command_num)

        """second pass."""
        self._parser = Parser(filename)
        hack_file_content = ""
        while self._parser.has_more_commands():
            self._parser.advance()
            return_value = {
                CommandType.C_COMMAND: lambda: self._assemble_c_command(),
                CommandType.A_COMMAND: lambda: self._assemble_a_command(),
                CommandType.L_COMMAND: lambda: self._assemble_l_command(),
            }[self._parser.command_type()]()

            hack_file_content += return_value + "\n" if return_value else ""

        _write_to_file(filename, hack_file_content)


    def _assemble_a_command(self):
        """
        Translates the A-instruction into machine language.
        :return: the translated value of the command
        """
        hack_line = "{0:b}".format(int(self._parser.symbol()))
        return hack_line.rjust(16, '0')

    def _assemble_l_command(self):
        """
        Translates the Location deceleration into machine language
        :return: the translated value of the command
        """
        if self._parser.is_label():
            return
        if not self._symbol_table.contains(self._parser.symbol()):
            self._symbol_table.addEntry(self._parser.symbol(), self._current_symbol_num)
            self._current_symbol_num += 1
        hack_line = "{0:b}".format(self._symbol_table.getAddress(self._parser.symbol()))
        while len(hack_line) < 16:
            hack_line = "0" + hack_line
        return hack_line

    def _assemble_c_command(self):
        """
        Translates the C-instruction into machine language.
        :return: the translated value of the command
        """
        hack_line = ""
        current_comp = self._parser.comp()
        current_dest = self._parser.dest()
        current_jump = self._parser.jump()
        hack_line += "101" if "<<" in current_comp or ">>" in current_comp else "111"
        hack_line += comp(current_comp)
        hack_line += dest(current_dest)
        hack_line += jump(current_jump)
        return hack_line

if __name__ == '__main__':
    main = Main()

    for arg_path in sys.argv:

        if isdir(arg_path):
            all_files = [join(arg_path, f) for f in listdir(arg_path) if isfile(join(arg_path, f))]
            files = [f for f in all_files if path.splitext(f)[1] == ".asm"]
        elif path.splitext(arg_path)[1] == ".asm":
            files = [arg_path]
        else:
            continue

        for file_runner in files:
            print("Processing the following file: {}".format(file_runner))
            main.parse_file(file_runner)
            print("Done processing {}\n~~~~~~~~~~~~~~".format(file_runner))