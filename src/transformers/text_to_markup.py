import re

from nodes.leafnode import LeafNode
from nodes.voidnode import VoidNode
from nodes.textnode import TextType

def text_to_html(text_node):
    """text_to_html converts TextNode into a LeafNode (child of HTMLNode)."""
    if not isinstance(text_node.text_type, TextType):
        raise ValueError("The text node's type must be an instance of textnode.TextType.")
    
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.LINEBREAK:
            return VoidNode("br", value="")
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={ "href": text_node.url })
        case TextType.IMAGE:
            return VoidNode("img", "", props={ "src": text_node.url, "alt": text_node.text})


def extract_markdown_images(text):
    """
    extract_markdown_images takes a raw markdown string and returns a list of tuples. Each tuple contains the alt text, URL, and title of any images found in the string.

    Example:

    ```python
    extract_markdown_images("Text ![alt text](https://example.png)")
    # returns [("alt text", "https://example.png")]
    ```

    Missing alt text or URL results in a tuple with empty strings. This may be
    changed at a later time.

    ```python
    extract_markdown_images("Empty ![]()")
    # returns [("", "")]
    ```
    """
    image_regex = r'!\[([^\[\]]*)\]\(([^\(\)]*)\)'
    matches = re.findall(image_regex, text)
    return matches



def extract_markdown_links(text):
    """
    extract_markdown_links takes a raw markdown string and returns a list of tuples. Each tuple contains the anchor text, URL, and title of any hyperlinks found in the string.

    ```python
    extract_markdown_links("Link [link](https://example.com)")
    # returns [("link", "https://example.com", "")]

    extract_markdown_links('Link [link](https://example.com "title")')
    # returns [("link", "https://example.com", "title")]
    ```

    Missing link text or URL results in a tuple with empty strings. This may be
    changed at a later time.

    ```python
    extract_markdown_images("Empty ![]()")
    # returns [("", "")]
    ```
    """
    link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*?)(?:\s+\"([^\"]*)\")?\)"
    matches = re.findall(link_regex, text)
    return matches