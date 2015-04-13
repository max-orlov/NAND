__author__ = 'maxorlov'
from Parser import Parser
if __name__ == '__main__':
    par = Parser('/media/maxorlov/UUI/NAND/projects/07/vm_impl/tester')
    while par.has_more_command():
        # print(par._current_line_index)
        par.advance()
        print("{}:::{}:::{}".format(par.command_type(), par.arg1(), par.arg2()))
