import unittest

from textnode import *


class Test_TextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_neg(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_value(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(str(node), "TextNode(This is a text node, bold, https://www.boot.dev)")

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(str(node), "TextNode(This is a text node, bold)")



class Test_TextNode_To_HTML(unittest.TestCase):
    def test_no_type_to_html_node(self):
        node = TextNode("This is a no type node", None)
        self.assertRaises(TypeError, node.to_html_node)

    def test_fake_type_to_html_node(self):
        node = TextNode("This is a no type node", "Foobar")
        self.assertRaises(TypeError, node.to_html_node)

    def test_text_to_html_node(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node.to_html_node().to_html(), 'This is a text node')

    def test_bold_to_html_node(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        self.assertEqual(node.to_html_node().to_html(), '<b>This is a bold node</b>')

    def test_italic_to_html_node(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        self.assertEqual(node.to_html_node().to_html(), '<i>This is an italic node</i>')

    def test_code_to_html_node(self):
        node = TextNode("This is a code node", TextType.CODE)
        self.assertEqual(node.to_html_node().to_html(), '<code>This is a code node</code>')

    def test_link_to_html_node(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node.to_html_node().to_html(), '<a href="https://www.boot.dev">This is a link node</a>')

    def test_image_to_html_node(self):
        node = TextNode("This is a image node", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp")
        self.assertEqual(node.to_html_node().to_html(), '<img src="https://www.boot.dev/img/bootdev-logo-full-small.webp" alt="This is a image node" />')



class Test_Split_Nodes_Delimiter(unittest.TestCase):
    def test_non_text_node(self):
        node = TextNode("This is bold text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is bold text", TextType.BOLD)])


    def test_bold_node(self):
        node = TextNode("This is text node with **bold text** inside", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text node with ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" inside", TextType.TEXT),
        ])
    
    def test_italic_node(self):
        node = TextNode("This is text node with *italic text* inside", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text node with ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" inside", TextType.TEXT),
        ])

    def test_code_node(self):
        node = TextNode("This is text node with a `code block` inside", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text node with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" inside", TextType.TEXT),
        ])

    def test_delim_bold_double(self):
        node = TextNode("This is text with a **bolded** word and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode("This is text with a **bolded word** and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )



if __name__ == "__main__":
    unittest.main()