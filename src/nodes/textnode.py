from enum import Enum

class TextType(Enum):
    """TextType is an Enum storing types for describing text."""
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    """
    TextNode represents a piece of text along with a text_type descriptor and
    optional url field for hyperlinks.

    In most cases, the only necessary inputs are the text and its type. IMAGE and LINK instances also expect a url, although a url of None is possible. For images, the text is an alternative text.

    To convert a TextNode to a LeafNode (child of HTMLNode), use text_to_html,
    found in text_to_markup.py.
    """
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text) and (self.text_type == other.text_type) and (self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
