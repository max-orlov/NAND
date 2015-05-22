from Tokenizer import tokenize
from Parser import parseTokens
import sys


in_stream = open(sys.argv[1])
s = "".join(in_stream.readlines())

out_stream = open("parser_out.txt", "w")
tokens = tokenize(s)
out_stream.write(parseTokens(tokens))
out_stream.close()