from pathlib import Path
import os
import shutil
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from markdown_blocks import markdown_to_html_node, markdown_to_blocks, block_to_block_type, BlockType

def copy_static_dir(source_dir, dest_dir):
        source_list = os.listdir(source_dir)
        for item in source_list:
            full_path = os.path.join(source_dir, item)
            if os.path.isfile(full_path):
                file_dest_path = os.path.join(dest_dir, item)
                shutil.copy(full_path, file_dest_path)
                print(f"Copying {full_path} to {file_dest_path}")
            else:
                file_dest_path = os.path.join(dest_dir, item)
                if not os.path.exists(file_dest_path):
                    os.mkdir(file_dest_path)
                    print(f"Creating Directory: {file_dest_path}")
                copy_static_dir(full_path, file_dest_path)

def extract_title(markdown):
    mblocks = markdown_to_blocks(markdown)
    for block in mblocks:
        if block_to_block_type(block) == BlockType.HEADING and block.startswith("# "):
            return block[2:].strip()
    raise ValueError("No h1 found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r", encoding="utf-8") as f:
        md = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        tpl = f.read()

    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    page = tpl.replace("{{ Title }}", title).replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, item)
        if os.path.isdir(full_path):
            dest_subdir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(full_path, template_path, dest_subdir)
        elif full_path.endswith(".md"):
            dest_file = os.path.join(dest_dir_path, os.path.splitext(item)[0] + ".html")
            generate_page(full_path, template_path, dest_file)


def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
        os.mkdir("./public")
    else:    
        os.mkdir("./public")
    
    copy_static_dir("./static", "./public")
    generate_pages_recursive("content/", "template.html", "public/")

    
main()