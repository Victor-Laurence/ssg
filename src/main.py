from htmlnode import *
from textnode import *

def main():
    testnode = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(testnode)

def text_node_to_html_node(text_node):
    if text_node.text_type == None: raise TypeError

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise TypeError

if __name__ == "__main__":
    main()