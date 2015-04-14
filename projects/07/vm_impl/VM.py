__author__ = 'Maxim'
from Parser import Parser
from CodeWriter import CodeWriter


class VM():

    def __init__(self):
        self._parser = Parser
        self._code_writer = CodeWriter

    def parse_file(self, file_name):
        pass
