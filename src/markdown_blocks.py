from enum import Enum
from htmlnode import *
from textnode import *
from inline_markdown import *


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown):
    md_blocks = markdown.split("\n\n")
    blocks = []
    for block in md_blocks:
        if block == "":
            continue
        block = block.strip()
        blocks.append(block)
    return blocks


def block_to_block_type(block):
    lines = block.split("\n")

    # Headings start with 1-6 # characters, followed by a space and then the heading text.
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    # Code blocks must start with 3 backticks and end with 3 backticks.
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    
    # Every line in a quote block must start with a > character.
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    # Every line in an unordered list block must start with a * or - character, followed by a space.
    if block.startswith("* "):
        for line in lines:
            if not block.startswith("* "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("- "):
        for line in lines:
            if not block.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST

    # Every line in an ordered list block must start with a number followed by a . character and a space. 
    # The number must start at 1 and increment by 1 for each line.
    if block.startswith("1. "):
        for i in range(len(lines) - 1):
            if not lines[i + 1].startswith(f"{i + 2}. "):
                return BlockType.PARAGRAPH
        return BlockType.OLIST

    # If none of the above conditions are met, the block is a normal paragraph.
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.OLIST:
            return olist_to_html_node(block)
        case BlockType.ULIST:
            return ulist_to_html_node(block)
    raise ValueError("Invalid block type")



def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node.to_html_node()
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)