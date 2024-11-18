import unittest

from htmlnode import *


class Test_HTMLNode(unittest.TestCase):
    def test_defaults(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_str_output(self):
        props = {
            "href": "https://www.google.com", 
            "target": "_blank",
        }
        node = HTMLNode("a", None, None, props)
        self.assertEqual(str(node), "HTMLNode(a, None, None, {'href': 'https://www.google.com', 'target': '_blank'})")

    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com", 
            "target": "_blank",
        }
        node = HTMLNode(None, None, None, props)
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank"')



class Test_ParentNode(unittest.TestCase):
    def test_defaults(self):
        leaf = LeafNode("", "")
        node = ParentNode("html", [leaf])
        self.assertEqual(node.tag, "html")
        self.assertEqual(node.value, None)
        self.assertTrue(len(node.children) == 1)
        self.assertEqual(node.props, None)

    def test_empty_tag(self):
        parent = ParentNode("", [LeafNode("","")])
        self.assertRaises(ValueError, parent.to_html)

    def test_no_children(self):
        parent = ParentNode("html", None)
        self.assertRaises(ValueError, parent.to_html)

    def test_has_children(self):
        leaf1 = LeafNode("b", "Bold text")
        leaf2 = LeafNode(None, "Normal text")
        leaf3 = LeafNode("i", "italic text")
        leaf4 = LeafNode(None, "Normal text")
        parent = ParentNode("p", [leaf1, leaf2, leaf3, leaf4])
        self.assertEqual(parent.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_has_otherchildren(self):
        leaf5 = LeafNode("h1", "Header text")
        leaf6 = LeafNode("h2", "Smaller header text")
        parent2 = ParentNode("h", [leaf5, leaf6])
        self.assertEqual(parent2.to_html(), '<h><h1>Header text</h1><h2>Smaller header text</h2></h>')

    def test_has_child_that_has_children(self):
        leaf1 = LeafNode("b", "Bold text")
        leaf2 = LeafNode(None, "Normal text")
        leaf3 = LeafNode("i", "italic text")
        leaf4 = LeafNode(None, "Normal text")
        parent1 = ParentNode("p", [leaf1, leaf2, leaf3, leaf4])
        
        leaf5 = LeafNode("h1", "Header text")
        leaf6 = LeafNode("h2", "Smaller header text")
        parent2 = ParentNode("h", [leaf5, leaf6])

        top_parent = ParentNode("html", [parent2, parent1])
        self.assertEqual(top_parent.to_html(), '<html><h><h1>Header text</h1><h2>Smaller header text</h2></h><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></html>')




class Test_LeafNode(unittest.TestCase):
    def test_defaults(self):
        leaf = LeafNode("", "")
        self.assertEqual(leaf.tag, "")
        self.assertEqual(leaf.value, "")
        self.assertEqual(leaf.children, None)
        self.assertEqual(leaf.props, None)

    def test_no_value(self):
        leaf = LeafNode("", None)
        self.assertRaises(ValueError, leaf.to_html)

    def test_empty_value_no_props(self):
        leaf = LeafNode("", "")
        self.assertRaises(ValueError, leaf.to_html)

    def test_empty_value_with_props(self):
        leaf = LeafNode("img", "", {"src": "https://www.boot.dev/img/bootdev-logo-full-small.webp"})
        self.assertEqual(leaf.to_html(), '<img src="https://www.boot.dev/img/bootdev-logo-full-small.webp" />')

    def test_value_only1(self):
        leaf = LeafNode("", "Some text")
        self.assertEqual(leaf.to_html(), "Some text")

    def test_value_only2(self):
        leaf = LeafNode(None, "Some text")
        self.assertEqual(leaf.to_html(), "Some text")

    def test_tag_value(self):
        leaf = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(leaf.to_html(), "<p>This is a paragraph of text.</p>")

    def test_tag_value_props(self):
        leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(leaf.to_html(), '<a href="https://www.google.com">Click me!</a>')



if __name__ == "__main__":
    unittest.main()