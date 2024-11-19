import unittest

from inline_markdown import *


class Test_Text_to_TextNodes(unittest.TestCase):
    def test_sample_text(self):
        self.assertTrue(True)
        #return
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_nodes
        )



class Test_Split_Nodes_Delimiter(unittest.TestCase):
    def test_non_text_node_already(self):
        node = TextNode("This is bold text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is bold text", TextType.BOLD)])


    def test_delim_bold(self):
        node = TextNode("This is text node with **bold text** inside", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text node with ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" inside", TextType.TEXT),
        ])
    
    def test_delim_italic(self):
        node = TextNode("This is text node with *italic text* inside", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text node with ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" inside", TextType.TEXT),
        ])

    def test_delim_code(self):
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
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes
        )

    def test_delim_bold_multiword(self):
        node = TextNode("This is text with a **bolded word** and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD)
            ],
            new_nodes
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes
        )



class Test_Extract_Markdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        tuples = extract_markdown_images(text)
        self.assertEqual(tuples, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        tuples = extract_markdown_links(text)
        self.assertEqual(tuples, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])



class Test_Split_Img_Lnk_Nodes(unittest.TestCase):
    def test_img_node_already(self):
        img_node = TextNode("This is a image node", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp")
        new_nodes = split_nodes_image([img_node])
        self.assertEqual(new_nodes, [img_node])

    def test_lnk_node_already(self):
        link_node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        new_nodes = split_nodes_image([link_node])
        self.assertEqual(new_nodes, [link_node])

    def test_img(self):
        node = TextNode(
           "This is text with an image ![Boot.Dev Logo](https://www.boot.dev/img/bootdev-logo-full-small.webp)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("Boot.Dev Logo", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp")
            ],
            new_nodes
        )

    def test_img_double(self):
        node = TextNode(
           "This is text with an image ![Boot.Dev Logo](https://www.boot.dev/img/bootdev-logo-full-small.webp) and ![Boots](https://www.boot.dev/_nuxt/new_boots_profile.DriFHGho.webp)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("Boot.Dev Logo", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp"),
                TextNode(" and ", TextType.TEXT),
                TextNode("Boots", TextType.IMAGE, "https://www.boot.dev/_nuxt/new_boots_profile.DriFHGho.webp")
            ],
            new_nodes
        )

    def test_link(self):
        node = TextNode(
           "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
            ],
            new_nodes
        )

    def test_link_double(self):
        node = TextNode(
           "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            new_nodes
        )

    def test_link_and_image(self):
        node = TextNode(
           "This is text with a link [to boot dev](https://www.boot.dev) and an image ![Boot.Dev Logo](https://www.boot.dev/img/bootdev-logo-full-small.webp)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and an image ", TextType.TEXT),
                TextNode("Boot.Dev Logo", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp")
            ],
            new_nodes
        )



if __name__ == "__main__":
    unittest.main()