from nodes.textnode import TextNode, TextType
from nodes.parentnode import ParentNode
from nodes.leafnode import LeafNode
from nodes.voidnode import VoidNode
from markdown_to_html_nodes.markdown_to_block_strings import markdown_to_block_strings
from markdown_to_html_nodes.block_to_block_type import block_to_block_type, BlockType
from markdown_to_html_nodes.text_to_textnodes import text_to_textnodes
from markdown_to_html_nodes.text_to_markup import text_to_html, extract_markdown_images


def markdown_to_html_node(markdown, parent_tag="div", parent_props=None):
    """markdown_to_html_node parses the markdown string into blocks and inline elements, wraps them in the parent node, and returns that node."""
    parent_node = ParentNode(parent_tag, children=[], props=parent_props)

    block_strings = markdown_to_block_strings(markdown)
    for str in block_strings:
        block_node = block_string_to_html_nodes(str)
        parent_node.children.append(block_node)

    return parent_node
        
def block_string_to_html_nodes(text):
    """block_string_to_html_nodes accepts a string of markdown, parses it, and returns a list of the corresponding HTML nodes."""
    block_type = block_to_block_type(text)
    match block_type:
        case BlockType.HEADING:   
            return make_heading_node(text)
        case BlockType.CODE:   
            return make_code_node(text)
        case BlockType.QUOTE:   
            return make_quote_node(text)
        case BlockType.IMAGE:
            return make_image_node(text)
        case BlockType.UNORDERED_LIST:   
            return make_list_node(text, tag="ul")
        case BlockType.ORDERED_LIST:   
            return make_list_node(text, tag="ol")
        case BlockType.PARAGRAPH:   
            return make_paragraph(text)

def make_node(tag, text):
    """
    make_node accepts a tag and some a markdown block string that is stripped of its block-identifying characters and returns an HTML node with that tag. The text is parsed by text_to_textnodes and text_to_html.

    If there's only one node in the resulting list, the node returned will be a LeafNode with the original text. Otherwise, a ParentNode will be returned with those children.
    """
    child_text_nodes = text_to_textnodes(text)

    if len(child_text_nodes) == 1 \
      and child_text_nodes[0].text_type == TextType.NORMAL:
        return LeafNode(tag, child_text_nodes[0].text)

    child_html_nodes = list(map(text_to_html, child_text_nodes))

    node = ParentNode(tag, child_html_nodes)
    return node

def make_heading_node(text):
    left, right = text.split(" ", maxsplit=1)
    tag = "h" + str(len(left))
    node = make_node(tag, right)
    return node

def make_code_node(text):
    code_text = text.strip("`")
    code_node = text_to_html(TextNode(code_text, TextType.CODE))
    return ParentNode("pre", children=[code_node])
    
def make_quote_node(text):
    """Split the text on newlines, strip whitespace, and remove the leading > from each line. The result is joined in new string, and empty lines are replaced with newline characters. These will be converted to <br> tags by text_to_html."""
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        line = line.strip()
        if len(line) == 1:
            new_lines.append("\n")
        else:
            new_lines.append(line.split(" ", maxsplit=1)[1])

    node = make_node("blockquote", "".join(new_lines))
    return node

def make_image_node(text, tag="img"):
    alt, src = extract_markdown_images(text)[0]
    return VoidNode(tag, props={ "src": src, "alt": alt })

def make_list_node(text, tag="ul"):
    lines = text.split("\n")
    list_item_text = [line.split(" ", maxsplit=1)[1] for line in lines]
    list_child_nodes = [make_node("li", text) for text in list_item_text]
    return ParentNode(tag, list_child_nodes)

def make_paragraph(text):
    return make_node("p", text)
