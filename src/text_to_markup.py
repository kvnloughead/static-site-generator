from leafnode import LeafNode
from textnode import TextNode, TextType

def text_to_html(text_node):
    """text_to_html converts TextNode into a LeafNode (child of HTMLNode)."""
    if not isinstance(text_node.text_type, TextType):
        raise ValueError("The text node's type must be an instance of textnode.TextType.")
    
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={ "href": text_node.url })
        case TextType.IMAGE:
            return LeafNode("img", "", props={ "src": text_node.url, "alt": text_node.text})    
