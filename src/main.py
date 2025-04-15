from textnode import *
from htmlnode import *

def main():
    test_node = TextNode("meow meow meow", TextType.LINK)
    test_html = HTMLNode("<meow>", "meow value", "meow children", {"href": "this is a url", "target": "this is a target"})
    print(test_node)
    print(test_html)
    print(test_html.props_to_html())

if __name__ == "__main__":
    main()