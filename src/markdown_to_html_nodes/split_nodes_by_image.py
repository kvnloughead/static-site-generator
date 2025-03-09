from nodes.textnode import TextNode, TextType
from markdown_to_html_nodes.text_to_markup import extract_markdown_images

def split_nodes_by_image(old_nodes, new_nodes=None):
    """
    split_nodes_by_image takes a list of nodes and splits any text nodes whenever it encounters a markdown image. Here is an example:

    ```python
    text_node = TextNode("Text ![alt](image.png) text.", TextType.NORMAL)
    node = LeafNode("p", "text")
    new_nodes = split_nodes_by_image([text_node, node])
    ```

    The new_nodes list will look like this:

    ```python
    [
        TextNode("Text", TextType.NORMAL),
        TextNode("alt", TextType.IMAGE, url="image.png"),
        TextNode(" text.", TextType.NORMAL),
        LeafNode("p", "text")
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
        images = extract_markdown_images(current_text)
        if len(images) == 0:
            result.append(current_node)
            return split_nodes_by_image(old_nodes[1:], result)
        for image in images:
            left, right = split_text_on_image(current_text, image)
            if left != "":
                result.append(TextNode(left, TextType.NORMAL))
            result.append(TextNode(image[0], TextType.IMAGE, url=image[1]))
            current_text = right
        if current_text != "":
            result.append(TextNode(right, TextType.NORMAL))
    return split_nodes_by_image(old_nodes[1:], result)

def split_text_on_image(text, image):
    """
    split_text_on_image splits a string using a markdown image as a delimiter.
    The maxsplits parameter is set to 1, so there are only two pieces: to the 
    left of the image and to the right. These are returned in a tuple.

    Parameters
    
    - text: a string of markdown
    - image: a tuple of two strings. The first will be used as the markdown 
             image's alt text, the second as its URL.
    """
    image_string = f"![{image[0]}]({image[1]})"
    left, right = text.split(image_string, 1)
    return (left, right)