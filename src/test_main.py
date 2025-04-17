import unittest

from main import text_node_to_html_node
from textnode import *

class TestMain(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("this is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "this is a bold node")

    def test_italics(self):
        node = TextNode("this is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "this is an italic node")

    def test_cold(self):
        node = TextNode("this is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "this is a code node")

    def test_link(self):
        node = TextNode("this is a link node", TextType.LINK, url="http://meowmix.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "this is a link node")
        self.assertEqual(html_node.props["href"], "http://meowmix.com")

    def test_image(self):
        node = TextNode("this is an image node", TextType.IMAGE, url="http://meowmix.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertIsNone(html_node.value)
        self.assertEqual(html_node.props["src"], "http://meowmix.com")
        self.assertEqual(html_node.props["alt"], "this is an image node")