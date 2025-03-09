class HTMLNode:
    """
    HTMLNode is the base class of representation of an HTML node. It is mostly
    used via subclasses:

    ParentNode - a node that has children
    LeafNode - a node that doesn't have children
    VoidNode - a self-closing LeafNode
    """
    _self_closing_tags = ["area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"]

    def __init__(self, tag=None, value=None, children=None, props=None):
        if tag in self._self_closing_tags and not self.is_void():
            raise TypeError(f"A {tag} tag is void and must be created as a VoidNode.")
        if not (tag or value or children):
            raise TypeError("Must provide at least one of tag, value, or children")
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props        

    def is_void(self):
        """is_void is only implemented by VoidNode."""
        pass

    def to_html(self):
        raise Exception(NotImplementedError)
    
    def props_to_html(self):
        if not self.props:
            return ""
        result = ""
        for name, val in self.props.items():
            result += f' {name}="{val}"'
        return result
    
    def _get_opening_tag(self):
        if not self.tag:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>"
    
    def _get_value(self, indent=None):
        if not self.value:
            return ""
        if indent:
            return f"\n{indent * " "}{self.value}"
        return self.value

    def _get_closing_tag(self):
        return f"</{self.tag}>"

    def _get_children(self):
        if not self.children:
            return ""
        result = ""
        for child in self.children:
            result += repr(child)
        return result

    def __repr__(self, self_closing=False):
        result = self._get_opening_tag()
        result += self._get_value()
        result += self._get_children()
        if not self_closing:
            result += self._get_closing_tag()
        return result

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and self.value == other.value and self.props == other.props and self.children == other.children)