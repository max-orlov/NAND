__author__ = 'Maxim'
from Tokenizer import tokenize
import sys


in_stream = open(sys.argv[1])
s = "".join(in_stream.readlines())


print(tokenize(s))