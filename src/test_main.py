import unittest

from main import *


class TestMain(unittest.TestCase):
    def test_no_type_to_html_node(self):
        node = TextNode("This is a no type node", None)
        self.assertRaises(TypeError, text_node_to_html_node, node)

    def test_fake_type_to_html_node(self):
        node = TextNode("This is a no type node", "Foobar")
        self.assertRaises(TypeError, text_node_to_html_node, node)

    def test_text_to_html_node(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(text_node_to_html_node(node).to_html(), 'This is a text node')

    def test_bold_to_html_node(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        self.assertEqual(text_node_to_html_node(node).to_html(), '<b>This is a bold node</b>')

    def test_italic_to_html_node(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        self.assertEqual(text_node_to_html_node(node).to_html(), '<i>This is an italic node</i>')

    def test_code_to_html_node(self):
        node = TextNode("This is a code node", TextType.CODE)
        self.assertEqual(text_node_to_html_node(node).to_html(), '<code>This is a code node</code>')

    def test_link_to_html_node(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(text_node_to_html_node(node).to_html(), '<a href="https://www.boot.dev">This is a link node</a>')

    def test_image_to_html_node(self):
        node = TextNode("This is a image node", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp")
        self.assertEqual(text_node_to_html_node(node).to_html(), '<img src="https://www.boot.dev/img/bootdev-logo-full-small.webp" alt="This is a image node" />')


if __name__ == "__main__":
    unittest.main()