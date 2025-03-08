from nodes.htmlnode import HTMLNode

class LeafNode(HTMLNode):
    """
    LeafNode is an HTMLNode containing text and no HTML element children. 
    Empty tags, like <div></div> are not LeafNodes. They can be created
    by the base HTMLNode class.

    Self-closing nodes are created with LeafNode's subclass VoidNode.

    Parameters
     - value is required but can be None.
     - tag is required but can be None.
    """
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        """
        If there is no value, a ValueError is raised. If there's no tag, the 
        value is returned as text. Otherwise, the parent's repr function is used.
        """
        if type(self.value) != str:
            raise ValueError("A leaf must have a value")
        if not self.tag:
            return self.value
        return self.__repr__()
    
    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return super().__eq__(other)

    def __str__(self, left_justify=0):
        if not self.tag:
            return self.to_html()
        return super().__str__(left_justify)
    
    def __repr__(self, self_closing=False):
        if not self.tag:
            return self.to_html()
        return super().__repr__(self_closing=self_closing)