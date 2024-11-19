from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks




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
    if block.startswith("* ") or block.startswith("- "):
        for line in lines:
            if not (block.startswith("* ") or block.startswith("- ")):
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