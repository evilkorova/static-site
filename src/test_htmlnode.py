import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_empty_props(self):
        node = HTMLNode("tag", "value", "children")
        self.assertEqual(node.props_to_html(), "")

    def test_single_props_key(self):
        node = HTMLNode("tag", "value", "children", {"href": "http://meowmix.com"})
        self.assertEqual(node.props_to_html(), ' href="http://meowmix.com"')

    def test_props_to_html_multiple_props(self):
        # Test with multiple props
        node = HTMLNode(
            "a", 
            "Click me", 
            None, 
            {"href": "http://google.com", "target": "_blank"}
        )
        self.assertTrue(' href="http://google.com"' in node.props_to_html())
        self.assertTrue(' target="_blank"' in node.props_to_html())

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

if __name__ == "__main__":
    unittest.main()