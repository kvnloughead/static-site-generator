from nodes.textnode import TextNode, TextType
from markdown_to_html_nodes.text_to_markup import extract_markdown_links

def split_nodes_by_link(old_nodes, new_nodes=None):
    """
    split_nodes_by_link takes a list of nodes and splits any text nodes whenever it encounters a markdown hyperlink. Here is an example:

    ```python
    text_node = TextNode("See [here](https://example.com) for no details.", TextType.NORMAL)
    node = LeafNode("p", "text")
    new_nodes = split_nodes_by_image([text_node, node])
    ```

    The new_nodes list will look like this:

    ```python
    [
        TextNode("See ", TextType.NORMAL),
        TextNode("here", TextType.LINK, url="https://example.com"),
        TextNode(" for no details..", TextType.NORMAL),
        LeafNode("p", "text")
    ]

    Limitations:

     - The extract_markdown_links function returns tuples with the link text, 
       URL, and the optional title field. split_nodes_by_link ignores the title.
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
        links = extract_markdown_links(current_text)
        if len(links) == 0:
            result.append(current_node)
            return split_nodes_by_link(old_nodes[1:], result)
        for link in links:
            left, right = split_text_on_link(current_text, link)
            if left != "":
                result.append(TextNode(left, TextType.NORMAL))
            result.append(TextNode(link[0], TextType.LINK, url=link[1]))
            current_text = right
        if current_text != "":
            result.append(TextNode(right, TextType.NORMAL))
    return split_nodes_by_link(old_nodes[1:], result)

def split_text_on_link(text, link):
    """
    split_text_on_link splits a string using a markdown link as a delimiter.
    The maxsplits parameter is set to 1, so there are only two pieces: to the 
    left of the link and to the right. These are returned in a tuple.

    Parameters

    - text: a string of markdown
    - link: a tuple of two strings. The first will be used as the link's text, 
    the second as its URL
    """
    link_string = f"[{link[0]}]({link[1]})"
    left, right = text.split(link_string, 1)
    return (left, right)