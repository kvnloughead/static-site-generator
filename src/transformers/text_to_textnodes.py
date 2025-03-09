from nodes.textnode import TextNode, TextType
from transformers.split_nodes_by_delimiter import split_nodes_by_delimiter
from transformers.split_nodes_by_image import split_nodes_by_image
from transformers.split_nodes_by_link import split_nodes_by_link
from transformers.split_nodes_by_linebreak import split_nodes_by_linebreak

delimiters = [
    ("**", TextType.BOLD),
    ("__", TextType.BOLD),
    ("*", TextType.ITALIC),
    ("_", TextType.ITALIC),
    ("`", TextType.CODE)
]

def text_to_textnodes(text):
    """
    text_to_textnodes takes a string of markdown text, splits it into separate text nodes (by delimiters, images, links, and line breaks), and returns a new list of text nodes.

    If the text is empty an exception is raised.
    """
    if len(text) == 0:
        raise Exception("Text nodes must not be empty")

    nodes = [TextNode(text, TextType.NORMAL)]
    with_delimiters = split_nodes_by_delimiters(nodes, delimiters)
    with_images = split_nodes_by_image(with_delimiters)
    with_links = split_nodes_by_link(with_images)
    with_linebreaks = split_nodes_by_linebreak(with_links)

    return with_linebreaks

def split_nodes_by_delimiters(nodes, delimiters):
    """Recursively split nodes by all delimiters in the list of delimiter tuples. """
    if len(delimiters) == 0:
        return nodes
    else:
        split_nodes = split_nodes_by_delimiter(nodes, *delimiters[0])
        return split_nodes_by_delimiters(split_nodes, delimiters[1:])