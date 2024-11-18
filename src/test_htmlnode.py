import unittest

from htmlnode import HTMLNode, LeafNode

# An HTMLNode without a tag will just render as raw text
# An HTMLNode without a value will be assumed to have children
# An HTMLNode without children will be assumed to have a value
# An HTMLNode without props simply won't have any attributes

class TestHTMLNode(unittest.TestCase):
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

class TestLeafNode(unittest.TestCase):
    def test_defaults(self):
        node = LeafNode("", "")
        self.assertEqual(node.tag, "")
        self.assertEqual(node.value, "")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_empty_value(self):
        node = LeafNode("", "")
        try:
            node.to_html()
        except Exception as e:
            self.assertEqual(e, ValueError)

    def test_value_only(self):
        node = LeafNode("", "Some text")
        self.assertEqual(node.to_html(), "Some text")

    def test_tag_value(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_tag_value_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

if __name__ == "__main__":
    unittest.main()