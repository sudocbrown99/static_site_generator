import os
import shutil
from textnode import TextNode, TextType

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

def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
        os.mkdir("./public")
    else:    
        os.mkdir("./public")
    
    copy_static_dir("./static", "./public")

    
main()