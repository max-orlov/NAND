__author__ = 'maxorlov'
from Parser import Parser
import sys

if __name__ == '__main__':
    par = Parser(sys.argv[1:])
    while par.has_more_command():
        # print(par._current_line_index)
        par.advance()
        print("{}:::{}:::{}".format(par.command_type(), par.arg1(), par.arg2()))
