import unittest

from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()