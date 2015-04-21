from os import path, getcwd, listdir
from os.path import isabs, abspath, join
from CodeWriter import CodeWriter
import sys

if __name__ == '__main__':
    dir_and_files = []
    for arg_path in sys.argv[1:]:
        # Getting absolute path for each dir
        dir_path = arg_path if isabs(arg_path) else abspath(path.join(getcwd(), arg_path))

        # Getting all files with '.vm' extension from that dir and adding the (dir:files) tuple to the list
        dir_and_files.append((dir_path, [file for file in listdir(dir_path) if path.splitext(file)[1] == '.vm']))

    for runner_dir_and_files in dir_and_files:
        dir_name = runner_dir_and_files[0]
        out_file_name = join(dir_name, path.basename(dir_name) + ".asm")
        cw = CodeWriter(out_file_name)
        print("====================\nWriting results into {}\n====================".format(out_file_name))
        for file_name in runner_dir_and_files[1]:
            print("Processing: {}".format(file_name))
            cw.set_file_name(join(dir_name, file_name))
            print("Processing Done :)")

        cw.close()
    print("<~~~~~~~~~~~~~~~~~~~~~>\nYou're all done :)")