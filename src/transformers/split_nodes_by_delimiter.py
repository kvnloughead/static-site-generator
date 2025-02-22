from nodes.textnode import TextNode, TextType

def split_nodes_by_delimiter(old_nodes, delimiter, text_type, new_nodes=None):
    """
    split_nodes_by_delimiter takes a list of nodes, splits any text nodes
    on the supplied delimiter, turns them into TextNodes, and returns a new list of nodes. An example will be worth all these words. Give this:

    ```python
    node = LeafNode("p", "text")
    text_node = TextNode("Text with a `code block` word", TextType.NORMAL)
    new_nodes = split_nodes_delimiter([text_node, node], "`", TextType.CODE)
    ```

    The new_nodes list will look like this:

    ```python
    [
        TextNode("This with a ", TextType.NORMAL),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.NORMAL),
        LeafNode("p", "text")
    ]
    ```
    """
    result = []
    if len(old_nodes) == 0 or (new_nodes != None and len(new_nodes) == 0):
        return new_nodes
    elif new_nodes:
        result = new_nodes.copy()
    
    current_node = old_nodes[0]

    # Add non-text nodes and text nodes with no value to the new list unchanged.
    if not isinstance(current_node, TextNode) or not current_node.text:
        result.append(current_node)
    else:
        split_nodes = split_node(current_node, delimiter, text_type)
        result.extend(split_nodes)
    return split_nodes_by_delimiter(old_nodes[1:], delimiter, text_type, result)
    

def split_node(text_node, delimiter, text_type):
    """
    split_node splits the given text node on the given delimiter. The delimiter
    can be one or more characters and are omitted from the result node's text. Guidelines followed:

    - Whitespace is always preserved, even if that's all that's in text segment
    - If the leftmost or rightmost segments are outside of a delimiter and empty, they are omitted
    - Empty pairs of delimiters are NOT omitted
    - If there is an unclosed delimiter, an exception is raised

     For example, calling `split_node(TextNode("ABC*DEF*XYZ), "*", TextType.ITALIC)` will return this:

    ```python
    [
        TextNode("ABC", TextType.NORMAL),
        TextNode("DEF", TextType.ITALIC)
        TextNode("XYZ", TextType.NORMAL)
    ]
    ```
    """
    if len(text_node.text) == 0:
        return []
    
    open_delimiter = False
    result_nodes = []
    curr_node = TextNode("", TextType.NORMAL) # default to normal

    i = 0
    if text_node.text[:len(delimiter)] == delimiter:
        i += len(delimiter)
        open_delimiter = True
        curr_node.text_type = text_type

    while i < len(text_node.text):
        char = text_node.text[i]
        # Opening delimiter found
        if text_node.text[i:i+len(delimiter)] == delimiter and not open_delimiter:
            # Add the current node to the results if it isn't empty
            if curr_node.text:
                result_nodes.append(curr_node)
            # Initialize the new current node with the new text type
            curr_node = TextNode("", text_type)
            i += len(delimiter) - 1
            open_delimiter = True
        
        # Closing delimiter found
        elif text_node.text[i:i+len(delimiter)] == delimiter:
            # Add the current node to the results if it isn't empty
            result_nodes.append(curr_node)
            # Reset open_delimiter and initialize the new current (normal) node
            open_delimiter = False
            curr_node = TextNode("", TextType.NORMAL)
            i += len(delimiter) - 1
        else:
            curr_node.text += char
        i += 1

    if open_delimiter > 0:
        raise Exception(f"Invalid markdown. No closing delimiter found, searching for \"{delimiter}\".")
    if curr_node.text:
        result_nodes.append(curr_node)
    return result_nodes
