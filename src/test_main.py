import unittest

from main import *


class Test_Main(unittest.TestCase):
    def test_extract_title(self):
        markdown = md = """
# Tolkien Fan Club

**I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)
"""
        title = extract_title(markdown)
        self.assertEqual(title, "Tolkien Fan Club")

    def test_extract_title_none_in_md(self):
        markdown = md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        self.assertRaisesRegex(ValueError, "No header found in markdown", extract_title, markdown)

if __name__ == "__main__":
    unittest.main()