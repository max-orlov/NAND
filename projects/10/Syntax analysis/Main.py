from os import path, getcwd, listdir
from os.path import isfile, isabs, abspath, normpath
from Tokenizer import tokenize
from Parser import parseTokens
import sys

if __name__ == '__main__':
    dir_and_files = []
    for arg_path in sys.argv[1:]:
        # Getting absolute path for each argument
        file_path = normpath(arg_path if isabs(arg_path) else abspath(path.join(getcwd(), arg_path)))
        if isfile(file_path):
            dir_and_files.append((path.split(file_path)[0], path.split(file_path)[1]))
        else:
            # Getting all files with '.jack' extension from that dir and adding the (dir:files) tuple to the list
            dir_and_files.append((file_path, [file for file in listdir(file_path) if path.splitext(file)[1] == '.jack']))

    for runner_dir_and_files in dir_and_files:
        dir_name = runner_dir_and_files[0]
        out_file_name = ""
        files_list = []
        if isinstance(runner_dir_and_files[1], list):
            files_list = runner_dir_and_files[1]
        else:
            files_list = [runner_dir_and_files[1],]

        for file_name in files_list:
            in_stream = open(path.join(dir_name, file_name))
            file_lines = "".join(in_stream.readlines())
            in_stream.close()
            tokens = tokenize(file_lines)

            out_file_name = path.splitext(file_name)[0]
            out_file_abs_name = path.join(dir_name, out_file_name + ".xml")
            out_stream = open(out_file_abs_name, "w")
            out_stream.write(parseTokens(tokens))
            out_stream.close()
    print("<~~~~~~~~~~~~~~~~~~~~~>\nYou're all done :)")