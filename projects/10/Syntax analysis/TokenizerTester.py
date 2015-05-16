from Tokenizer import tokenize
import sys


in_stream = open(sys.argv[1])
s = "".join(in_stream.readlines())

out_stream = open("token_out.txt", "w")
out_stream.write(tokenize(s))