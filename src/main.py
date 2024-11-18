from htmlnode import *
from textnode import *

def main():
    testnode = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(testnode)

if __name__ == "__main__":
    main()