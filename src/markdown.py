from enum import Enum
from htmlnode import *
from textnode import *
import re

class BlockType(Enum):
    PGRAPH = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    LIST = "unordered list"
    NUM = "ordered list"

def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        if block == "":
            continue
        blocks.append(block.strip())
    return blocks

def block_to_block_type(block):
    if block[0] == "#":
        return BlockType.HEAD
    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    if block[0] == ">":
        return BlockType.QUOTE
    if block[0] == "-":
        return BlockType.LIST
    if re.search("\d+\.\s", block):
        return BlockType.NUM
    else:
        return BlockType.PGRAPH
    
def block_to_child_nodes(text):
    child_nodes = text_to_textnodes(text)
    leaf_nodes = []
    for child in child_nodes:
        leaf = text_node_to_html_node(child)
        leaf_nodes.append(leaf)
    return leaf_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PGRAPH:
                text = block.replace("\n", " ")
                children = block_to_child_nodes(text)
                tag = "p"
            case BlockType.HEAD:
                block_split = block.split(" ",1)
                head_len = len(block_split[0])
                tag = f"h{head_len}"
                text = block_split[1]
                children = block_to_child_nodes(text)
            case BlockType.CODE:
                tag = "pre"
                text = block.lstrip("```\n")
                text = text.rstrip("```")
                child_text = TextNode(text, TextType.CODE)
                children = [text_node_to_html_node(child_text)]
            case BlockType.QUOTE:
                tag = "blockquote"
                text = block.lstrip(">")
                children = block_to_child_nodes(text)
            case BlockType.LIST:
                tag = "ul"
                line_list = block.split("\n")
                children = []
                for line in line_list:
                    if line == "":
                        continue
                    item = line.lstrip(">")
                    item = item.strip()
                    grandchildren = block_to_child_nodes(item)
                    children.append(ParentNode("li", grandchildren))
            case BlockType.NUM:
                tag = "ol"
                line_list = block.split("\n")
                children = []
                for line in line_list:
                    if line == "":
                        continue
                    item = line.lstrip(r"\d+\.")
                    item = item.strip()
                    grandchildren = block_to_child_nodes(item)
                    children.append(ParentNode("li", grandchildren))                
        block_node = ParentNode(tag, children)
        block_children.append(block_node)
    return ParentNode("div", block_children)

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