from textnode import *
from htmlnode import *
from markdown import *
from shutil import rmtree
from shutil import copy
import os


def main():
    copy_dir("static", "public")


def copy_dir(src, dst):
    # check and delete everything in dst
    if not os.path.exists(dst):
        raise Exception(f"destination {dst} does not exist")
    print(f"deleting {dst}")
    rmtree(dst)
    os.mkdir(dst)
    recursive_copy(src, dst)

def recursive_copy(src, dst):
    for path in os.listdir(src):
        src_path = os.path.join(src, path)
        if os.path.isfile(src_path):
            print(f"copying {src_path} to {dst}")
            copy(src_path, dst)
        elif os.path.isdir(src_path):
            recursive_copy(src_path, os.path.join(dst, path))
        else:
            raise Exception(f"{src_path} is not file or directory")
        
if __name__ == "__main__":
    main()