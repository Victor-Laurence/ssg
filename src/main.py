import os
import shutil

def main():
    root = os.getcwd()
    static = os.path.join(root, "static")
    public = os.path.join(root, "public")

    clean_dir(public)
    copy_dir(static, public)


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


if __name__ == "__main__":
    main()