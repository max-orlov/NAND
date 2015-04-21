__author__ = 'Maxim'
from os import path, getcwd, listdir
from os.path import isabs, abspath, join
import glob
from fnmatch import filter
from CodeWriter import CodeWriter
import sys

if __name__ == '__main__':
    dir_and_files = []
    for arg_path in sys.argv[1:]:
        files = []
        # Getting absolute path for each dir
        dir_path = arg_path if isabs(arg_path) else abspath(path.join(getcwd(), arg_path))
        files.extend([file for file in listdir(dir_path) if file.endswith(".vm")])
        dir_and_files.append([dir_path, files])

    for runner_dir_and_files in dir_and_files:
        out_file_name = join(runner_dir_and_files[0], path.basename(path.normpath(runner_dir_and_files[0]) + ".asm"))
        cw = CodeWriter(out_file_name)
        print("====================\nWriting results into {}\n====================".format(out_file_name))
        for file in runner_dir_and_files[1]:
            print("Processing: {}".format(join(runner_dir_and_files[0], file)))
            cw.set_file_name(join(runner_dir_and_files[0], path.splitext(file)[0] + ".vm"))
            print("Done ;)")

        cw.close()