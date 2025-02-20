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

def split_nodes_by_delimiter(old_nodes, delimiter, text_type, new_nodes=None):
    """
    split_nodes_by_delimiter takes a list of nodes, splits any text nodes
    on the supplied delimiter, turns them into TextNodes, and returns a new list of nodes. An example will be worth all these words. Give this:

    ```python
    node = LeafNode("p")
    text_node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([text_node, node], "`", TextType.CODE)
    ```

    The new_nodes list will look like this:

    ```python
    [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
        LeafNode("p")
    ]
    ```
    """
    if len(result) == 0:
        return result
    
    result = new_nodes.copy()
    current_node = old_nodes[0]

    # Add non-text nodes and text nodes with no value to the new list unchanged.
    if not isinstance(current_node, TextNode) or not current_node.value:
        result.append(current_node)
    else:
        split_nodes = split_node(current_node, delimiter, text_type)
        result.extend(split_nodes)
    return split_nodes_by_delimiter(old_nodes[1:], delimiter, text_type, result)
    

def split_node(text_node, delimiter, text_type):
    """
    split_node splits the given text node on the given delimiter. See 
    split_nodes_by_delimiter for examples.
    """
    if len(text_node.text) == 0:
        return []
    
    open_delimiter = False
    result_nodes = []
    curr_node = TextNode("", TextType.NORMAL) # default to normal

    for i, char in enumerate(text_node.text):
        # Opening delimiter found
        if text_node.text[i:i+len(delimiter)] == delimiter and not open_delimiter:
            # Add the current node to the results if it isn't empty
            if curr_node.text:
                result_nodes.append(curr_node)
            # Initialize the new current node with the new text type
            curr_node = TextNode("", text_type)
            open_delimiter = True
        
        # Closing delimiter found
        elif text_node.text[i:i+len(delimiter)] == delimiter:
            # Add the current node to the results if it isn't empty
            print(i, curr_node)
            if curr_node.text:
                result_nodes.append(curr_node)
            # Reset open_delimiter and initialize the new current (normal) node
            open_delimiter = False
            curr_node = TextNode("", TextType.NORMAL)
        else:
            curr_node.text += char
    
    if open_delimiter > 0:
        raise Exception(f"Invalid markdown. No closing delimiter found, searching for \"{delimiter}\".")
    
    result_nodes.append(curr_node)
    return result_nodes