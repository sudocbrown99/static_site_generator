import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invlaid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        extracted_markdown = extract_markdown_images(old_node.text)
        if extracted_markdown == []:
            new_nodes.append(old_node)
            continue
        remaining = old_node.text
        for (alt, link) in extracted_markdown:
            left, right = remaining.split(f"![{alt}]({link})", 1)
            if left:
                new_nodes.append(TextNode(left, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, link))
            remaining = right
        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes
         
def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        extracted_markdown = extract_markdown_links(old_node.text)
        if extracted_markdown == []:
            new_nodes.append(old_node)
            continue
        remaining = old_node.text
        for (name, link) in extracted_markdown:
            left, right = remaining.split(f"[{name}]({link})", 1)
            if left:
                new_nodes.append(TextNode(left, TextType.TEXT))
            new_nodes.append(TextNode(name, TextType.LINK, link))
            remaining = right
        if right:
            new_nodes.append(TextNode(right, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = (split_nodes_delimiter(nodes, "**", TextType.BOLD))
    nodes = (split_nodes_delimiter(nodes, "_", TextType.ITALIC))
    nodes = (split_nodes_delimiter(nodes, "`", TextType.CODE))
    nodes = (split_nodes_image(nodes))
    nodes = (split_nodes_link(nodes))
    return nodes
