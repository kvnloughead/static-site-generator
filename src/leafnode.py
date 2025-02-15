from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    """
    LeafNode is an HTMLNode containing text and no HTML element children. 
    Self-closing tags are not LeafNode, they are handled by VoidNode.
    Empty tags, like <div></div> are also not LeafNodes. They can be created
    by the base HTMLNode class.

    Parameters
     - value is required, and if it is None a ValueError is raised.
     - tag is required but can be None, in which case value is returned as text.
    """
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)
        if not self.value:
            raise ValueError("A leaf must have a value")

    def to_html(self):
       
        if not self.tag:
            return self.value
        return self.__repr__()