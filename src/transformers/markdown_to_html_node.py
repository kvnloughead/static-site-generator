from nodes.textnode import TextNode, TextType
from nodes.parentnode import ParentNode
from nodes.leafnode import LeafNode
from transformers.blocks import markdown_to_block_strings, block_to_block_type, BlockType
from transformers.text_to_textnodes import text_to_textnodes
from transformers.text_to_markup import text_to_html

def markdown_to_html_node(markdown, parent_tag="div", parent_props=None):
    """markdown_to_html_node parses the markdown string into blocks and inline elements, wraps them in the parent node, and returns that node."""
    parent_node = ParentNode(parent_tag, props=parent_props)
    children = []

    block_strings = markdown_to_block_strings(markdown)
    for bs in block_strings:
        children.extend(block_string_to_html_nodes(bs))
        
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
        case BlockType.UNORDERED_LIST:   
            return make_list_node(text, tag="ul")
        case BlockType.ORDERED_LIST:   
            return make_list_node(text, tag="ol")
        case BlockType.PARAGRAPH:   
            return make_paragraph(text)
        
def make_heading_node(text):
    left, right = text.split(" ", maxsplit=1)
    tag = "h" + str(len(left))
    child_text_nodes = text_to_textnodes(right)

    # One child should only occur if it is a normal text node.
    if len(child_text_nodes) == 1:
        return LeafNode(tag, right)

    child_html_nodes = list(map(text_to_html, child_text_nodes))
    node = ParentNode(tag, child_html_nodes)
    return node

def make_code_node(text):
    code_text = text.strip("`")
    code_node = text_to_html(TextNode(code_text, TextType.CODE))
    return ParentNode("pre", children=[code_node])
    
def make_quote_node(text):
    _, quote_text = text.split(" ", maxsplit=1)
    tag = "blockquote"
    child_text_nodes = text_to_textnodes(quote_text)

    # One child should only occur if it is a normal text node.
    if len(child_text_nodes) == 1:
        return LeafNode(tag, quote_text)

    child_html_nodes = list(map(text_to_html, child_text_nodes))
    node = ParentNode(tag, child_html_nodes)
    return node


def make_list_node(text, tag="ul"):
    lines = text.split("\n")
    list_item_text = [line.split(" ", maxsplit=1)[1] for line in lines]
    list_item_text_nodes = [text_to_textnodes(li) for li in list_item_text]
    list_item_child_nodes = [list(map(text_to_html, li)) 
                             for li in list_item_text_nodes]
    
    list_child_nodes = []
    for child_group in list_item_child_nodes:
        if len(child_group) == 1:
            list_child_nodes.append(LeafNode("li", child_group[0].value))
        else:
            list_child_nodes.append(ParentNode("li", child_group))

    return ParentNode(tag, list_child_nodes)

def make_paragraph(text):
    return LeafNode("p", text)
