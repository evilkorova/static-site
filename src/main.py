from textnode import *
from htmlnode import *
from markdown import *
from shutil import rmtree
from shutil import copy
import os


def main():
    copy_dir("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


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
            dst_path = os.path.join(dst, path)
            os.mkdir(dst_path)
            recursive_copy(src_path, dst_path)
        else:
            raise Exception(f"{src_path} is not file or directory")

def read_file(path):
    if not os.path.isfile(path):
        raise Exception(f"{path} is not a file")
    with open(path, "r") as file:
        text = file.read()
    return text

def generate_page(from_path, template_path, dest_path):
    print(f"generating page from {from_path} to {dest_path} using template {template_path}")
    content = read_file(from_path)
    template = read_file(template_path)
    html_node = markdown_to_html_node(content)
    #debug remove
    print(html_node)
    html = html_node.to_html()
    title = extract_title(content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    # check for created directories
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, "w") as file:
        file.write(template)

    

if __name__ == "__main__":
    main()