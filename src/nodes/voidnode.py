from test_utils import TestRunner
from nodes.leafnode import LeafNode

class VoidNode(LeafNode):
    """
    VoidNode is a self-closing leaf node. It has no children, and no closing tag. Examples include <img> and <input>.

    The tag parameter is required, and value must be an empty string.
    """
    def __init__(self, tag, value, props=None):
        if not tag:
            raise TypeError("A VoidNode must have a tag.")
        super().__init__(tag, value, props=props)

    def to_html(self):
        """
        If there is no value, a TypeError is raised. If there's no tag, the 
        value is returned as text. Otherwise, the parent's repr function is used.
        """
        return self.__repr__()
    
    def __repr__(self):
        return super().__repr__(self_closing=True)