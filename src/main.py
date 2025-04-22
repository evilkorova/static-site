from textnode import *
from htmlnode import *
import re


def main():
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
    test_node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([test_node], "`", TextType.CODE)
    print(new_nodes)
    test_mdimage = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(test_mdimage))
    image_node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) yep meow",
        TextType.TEXT,
    )
    new_image_nodes = split_nodes_image([image_node])
    print(new_image_nodes)
    link_node = TextNode(
        "This is text with an [bunch of links](https://i.imgur.com/zjjcJKZ.png) and another ![second link](https://i.imgur.com/3elNhQu.png) yep meow",
        TextType.TEXT,
    )
    new_link_nodes = split_nodes_link([link_node])
    print(new_link_nodes, "\n")
    big_test = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    big_test_nodes = text_to_textnodes(big_test)
    for test in big_test_nodes:
        print(test)

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("TextType not found")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception(f"matching closing delimiter: {delimiter} not found")
        split_node = node.text.split(delimiter)
        i = 0
        for s in split_node:
            if i % 2 == 0:
                new_nodes.append(TextNode(s, TextType.TEXT))
            else:
                new_nodes.append(TextNode(s, text_type))
            i += 1
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches
        

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        original_text = node.text
        images = extract_markdown_images(original_text)
        if not images:
            new_nodes.append(node)
        i = 1
        for image in images:
            image_alt = image[0]
            image_link = image[1]
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)
            if len(sections) == 2:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            if i == len(images) and sections[1] != "":
                new_nodes.append(TextNode(sections[1], TextType.TEXT))
            else:
                original_text = sections[1]
            i += 1      
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        original_text = node.text
        links = extract_markdown_links(original_text)
        if not links:
            new_nodes.append(node)
        i = 1
        for link in links:
            link_text = link[0]
            link_url = link[1]
            sections = original_text.split(f"[{link_text}]({link_url})", 1)
            if len(sections) == 2:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            if i == len(links) and sections[1] != "":
                new_nodes.append(TextNode(sections[1], TextType.TEXT))
            else:
                original_text = sections[1]
            i += 1      
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

if __name__ == "__main__":
    main()