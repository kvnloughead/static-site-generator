from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    """
    A ParentNode is an HTMLNode with children. If a node is not a ParentNode,
    it is a LeafNode. A ParentNode must be passed a tag and at least one child. The value argument is not specified.

    Note to self: three cases are still unclear to me as I follow along with the
    project. 
    
    (1) What about self-closing tags? It appears they would be a third
    possibility. 

    (2) Tags can have a value (which is text content, as I understand it) and
    children at the same time.

    (3) Non-self-closing tags also can have neither. For example: <div></div>.
    """
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("A tag must be specified")
        if not self.children:
            raise ValueError("A parent node must have children")
        return super().__repr__()
                
