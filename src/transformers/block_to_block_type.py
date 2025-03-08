import re
from enum import Enum

class BlockType(Enum):
    """
    BlockType is an enum storing supported types of markdown blocks.
    """
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"

def block_to_block_type(block_text):
    """
    block_to_block_type accepts a block of markdown text and return its block type, as an instance of the BlockType enum.

    All leading and trailing whitespace should be stripped from the text by the
    calling code.

    Supported types:

    - Headings start with 1 to 6 # characters, followed by a space, then one or more characters. Example: "# Foobar".
    - Code blocks start and end with three backticks. Example: "```\nprint("foobar")\n```. Newlines are allowed, but not required.
    - Quote: each line starts with a >.
    - Unordered list: each line starts with a * or each line starts with a -, followed by a space.
    - Ordered list: each line starts with a number followed by a "." character, followed by a space. The numbers must start at 1 and be sequential.
    """
    
    def is_unordered_list(lines):
        return each_line_starts_with("* ", lines) or each_line_starts_with("- ", lines)

    def is_quote(lines):
        for line in lines:
            if not (line.startswith("> ") or line == ">"):
                return False
        else:
            return True
    
    lines = block_text.split("\n")
    code_block_rx = re.compile(r'^```.+```$', re.DOTALL)
    heading_rx = r'^#{1,6}\s+.+'
    
    if re.match(heading_rx, block_text):
        return BlockType.HEADING
    elif re.match(code_block_rx, block_text):
        return BlockType.CODE
    elif is_quote(lines):
        return BlockType.QUOTE
    elif is_unordered_list(lines):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(lines):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def each_line_starts_with(char, lines):
    return all(line.startswith(char) for line in lines)

def is_ordered_list(lines, i=0):
    # Return True if all lines are processed successfully
    if i >= len(lines):
        return True
    
    # Return False if the current line does start with the right number
    if not lines[i].startswith(f"{i+1}. "):
        return False
        
    # Check the next line
    return is_ordered_list(lines, i+1)