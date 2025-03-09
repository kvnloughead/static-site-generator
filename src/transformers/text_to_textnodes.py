from nodes.textnode import TextNode, TextType
from transformers.split_nodes_by_delimiter import split_nodes_by_delimiter
from transformers.split_nodes_by_image import split_nodes_by_image
from transformers.split_nodes_by_link import split_nodes_by_link
from transformers.split_nodes_by_linebreak import split_nodes_by_linebreak

def text_to_textnodes(text):
    """
    text_to_textnodes takes a string of markdown and returns a list of textnodes.

    If text is the empty string an exception is raised.
    """
    if len(text) == 0:
        raise Exception("Text must not be empty")
    with_bold = split_nodes_by_delimiter([TextNode(text, TextType.NORMAL)], "**" ,TextType.BOLD)
    with_italic = split_nodes_by_delimiter(with_bold, "*", TextType.ITALIC)
    with_code = split_nodes_by_delimiter(with_italic, "`", TextType.CODE)
    with_images = split_nodes_by_image(with_code)
    with_links = split_nodes_by_link(with_images)
    with_linebreaks = split_nodes_by_linebreak(with_links)
    return with_linebreaks