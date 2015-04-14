__author__ = 'Maxim'
from VMStack import VMStack
from Parser import Parser
from CodeWriter import CodeWriter


class VM():

    def __init__(self):
        self._command_stack = VMStack
        self._parser = Parser
        self._code_writer = CodeWriter
