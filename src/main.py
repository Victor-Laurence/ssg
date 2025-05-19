import os
import shutil
import sys
from markdown_blocks import *

def main():
    basepath = "/"
    if len(sys.argv) > 1: 
        basepath = sys.argv[1]

    root = os.getcwd()
    static = os.path.join(root, "static")
    public = os.path.join(root, "public")
    content = os.path.join(root, "content")
    template = os.path.join(root, "template.html")
    public = os.path.join(root, "docs")

    clean_dir(public)
    copy_dir(static, public)
    print("*******************************************************************************")
    generate_pages_recursive(basepath, content, template, public)
    print("*******************************************************************************")


def clean_dir(public):
    if os.path.exists(public):
        shutil.rmtree(public)
    if not os.path.exists(public):
        os.mkdir(public)    


def copy_dir(source, destination):
    for path in os.listdir(source):
        full_source_path = os.path.join(source, path)
        full_dest_path = os.path.join(destination, path)

        if os.path.isdir(full_source_path):
            os.mkdir(full_dest_path)
            copy_dir(full_source_path, full_dest_path)
        elif os.path.isfile(full_source_path):
            shutil.copy(full_source_path, full_dest_path)


def extract_title(markdown):
    for block in markdown_to_blocks(markdown):
        lines = block.split("\n")
        for line in lines:
            if line.startswith("# "):
                return line[2:]
    raise ValueError("No header found in markdown")


def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    for path in os.listdir(dir_path_content):
        full_source_path = os.path.join(dir_path_content, path)
        full_dest_path = os.path.join(dest_dir_path, path)

        if os.path.isdir(full_source_path):
            os.mkdir(full_dest_path)
            generate_pages_recursive(basepath, full_source_path, template_path, full_dest_path)
        elif os.path.isfile(full_source_path):
            generate_page(basepath, full_source_path, template_path, full_dest_path.replace(".md", ".html"))


def generate_page(basepath, source_path, template_path, dest_path):
    print(f"Generating page from {source_path}\nto {dest_path}\nusing {template_path}\n")
    
    markdown = ""
    template = ""
    with open(source_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()
    
    title = extract_title(markdown)
    node = markdown_to_html_node(markdown)
    content = node.to_html()
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    html = html.replace('href="/', 'href="' + basepath).replace('src="/', 'src="' + basepath)

    with open(dest_path, "w") as file:
        file.write(html)

if __name__ == "__main__":
    main()