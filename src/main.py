from textnode import *
from htmlnode import *

def main():
    test_node = TextNode("meow meow meow", TextType.LINK)
    test_html = HTMLNode("<meow>", "meow value", "meow children", {"href": "this is a url", "target": "this is a target"})
    print(test_node)
    print(test_html)
    print(test_html.props_to_html())
    test_leaf = LeafNode("p", "This is a paragraph of text.").to_html()
    print(test_leaf)
    test_leaf_props = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
    print(test_leaf_props)
    print("\nParent Node Test")
    test_parent = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
    print(test_parent.to_html())



if __name__ == "__main__":
    main()