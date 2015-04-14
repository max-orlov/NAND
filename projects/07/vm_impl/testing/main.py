__author__ = 'maxorlov'
from Parser import Parser
from CodeWriter import CodeWriter
import sys

if __name__ == '__main__':
    cw = CodeWriter(sys.argv[1])
    cw.set_file_name(sys.argv[2])

