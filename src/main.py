import os
import shutil
from markdown_blocks import *

def main():
    root = os.getcwd()
    static = os.path.join(root, "static")
    public = os.path.join(root, "public")
    markdown = os.path.join(root, "content/index.md")
    template = os.path.join(root, "template.html")
    html = os.path.join(root, "public/index.html")

    clean_dir(public)
    copy_dir(static, public)
    generate_page(markdown, template, html)


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


def generate_page(from_path, template_path, dest_path):
    print("*******************************************************************************")
    print(f"Generating page from {from_path}\nto {dest_path}\nusing {template_path}")
    print("*******************************************************************************")
    
    markdown = ""
    template = ""
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()
    
    title = extract_title(markdown)
    node = markdown_to_html_node(markdown)
    content = node.to_html()
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    with open(dest_path, "w") as file:
        file.write(html)

if __name__ == "__main__":
    main()