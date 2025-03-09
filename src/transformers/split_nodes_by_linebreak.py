from nodes.textnode import TextNode, TextType
from nodes.voidnode import VoidNode

def split_nodes_by_linebreak(old_nodes, new_nodes=None):
    """
    split_nodes_by_linebreak takes a list of nodes and splits any text nodes whenever it encounters a single newline character. Here is an example:

    ```python
    text_node = TextNode("This text has\na line break", TextType.NORMAL)
    new_nodes = split_nodes_by_linebreak([text_node])
    ```

    The new_nodes list will look like this:

    ```python
    [
        TextNode("This line has", TextType.NORMAL),
        TextNode("\n", TextType.LINEBREAK)
        TextNode("a line break", TextType.NORMAL)
    ]
    ```
    """
    result = []
    if len(old_nodes) == 0 or (new_nodes != None and len(new_nodes) == 0):
        return new_nodes or []
    elif new_nodes:
        result = new_nodes.copy()
    
    current_node = old_nodes[0]
    if not isinstance(current_node, TextNode) or not current_node.text:
        result.append(current_node)
    else:
        current_text = current_node.text
        if not "\n" in current_text:
            result.append(current_node)
            return split_nodes_by_linebreak(old_nodes[1:], result)
        left, right = current_text.split("\n", maxsplit=1)
        if left != "":
            result.append(TextNode(left, TextType.NORMAL))
        result.append(TextNode("\n", TextType.LINEBREAK))
        if right != "":
            result.append(TextNode(right, TextType.NORMAL))
    return split_nodes_by_linebreak(old_nodes[1:], result)