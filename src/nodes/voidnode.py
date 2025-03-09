from nodes.leafnode import LeafNode

class VoidNode(LeafNode):
    """
    VoidNode is a self-closing leaf node. It has no children, no text content, and no closing tag. Examples include <img> and <input>.

    The tag parameter is required and can't be None and props are optional.
    """
    def __init__(self, tag, props=None):
        if not tag:
            raise TypeError("A VoidNode must have a tag.")
        super().__init__(tag, value=None, props=props)

    def to_html(self):
        return self.__repr__()
    
    def is_void(self):
        return True

    def __repr__(self):
        return super().__repr__(self_closing=self.is_void())