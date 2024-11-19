import os
import shutil

def main():
    #clean_public()
    #copy_static_files()
    pass


def clean_public():
    root = os.getcwd()
    public = os.path.join(root, "public")

    print(public)
    print(os.path.exists(public))
    if os.path.exists(public):
        shutil.rmtree(public)
    print(os.path.exists(public))
    if not os.path.exists(public):
        os.mkdir(public)
    print(os.path.exists(public))
    

def copy_static_files():
    pass



if __name__ == "__main__":
    main()