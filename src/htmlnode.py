class HTMLNode:
    """
    HTMLNode is the base class of representation of an HTML node. It is mostly
    used via subclasses.
    """
    def __init__(self, tag=None, value=None, children=None, props=None):
        if not (tag or value or children):
            raise TypeError("Must provide at least one of tag, value, or children")
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props        

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

    def _get_closing_tag(self, left_justify=None):
        if left_justify != None:
            return f"\n{left_justify * " "}</{self.tag}>"
        return f"</{self.tag}>"

    def _get_children(self, left_justify=None):
        if not self.children:
            return ""
        result = ""
        for child in self.children:
            if left_justify:
                result += f"\n{child.__str__(left_justify)}"
            else:
                result += repr(child)
        return result
        
    def __str__(self, left_justify=0):
        # Pretty printed version
        left_justify_spaces = left_justify * " "
        indent = (left_justify + 2)
        
        result = f"{left_justify_spaces}{self._get_opening_tag()}"
        result += self._get_value(indent)
        result += self._get_children(left_justify + 2)
        result += self._get_closing_tag(left_justify)
        return result

    def __repr__(self):
        # Raw HTML version
        result = self._get_opening_tag()
        result += self._get_value()
        result += self._get_children()
        result += self._get_closing_tag()
        return result