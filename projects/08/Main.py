from os import path, getcwd, listdir
from os.path import isfile, isabs, abspath, normpath
from CodeWriter import CodeWriter
import sys

if __name__ == '__main__':
    dir_and_files = []
    for arg_path in sys.argv[1:]:
        # Getting absolute path for each argument
        file_path = normpath(arg_path if isabs(arg_path) else abspath(path.join(getcwd(), arg_path)))
        if isfile(file_path):
            dir_and_files.append((path.split(file_path)[0], path.split(file_path)[1]))
        else:
            # Getting all files with '.vm' extension from that dir and adding the (dir:files) tuple to the list
            dir_and_files.append((file_path, [file for file in listdir(file_path) if path.splitext(file)[1] == '.vm']))

    for runner_dir_and_files in dir_and_files:
        dir_name = runner_dir_and_files[0]
        out_file_name = ""
        files_list = []
        if isinstance(runner_dir_and_files[1], list):
            out_file_name = path.basename(dir_name)
            files_list = runner_dir_and_files[1]
        else:
            out_file_name = path.splitext(runner_dir_and_files[1])[0]
            files_list = [runner_dir_and_files[1],]

        out_file_abs_name = path.join(dir_name, out_file_name + ".asm")
        cw = CodeWriter(out_file_abs_name)
        print("====================\nWriting results into {}\n====================".format(out_file_abs_name))
        for file_name in files_list:
            print("Processing: {}".format(file_name))
            cw.set_file_name(path.join(dir_name, file_name))
            print("Processing Done :)")

        cw.close()
    print("<~~~~~~~~~~~~~~~~~~~~~>\nYou're all done :)")