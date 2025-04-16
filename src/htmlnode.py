from enum import Enum

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise Exception(NotImplementedError)

    def props_to_html(self):
        result = ""
        if self.props is not None:
            for key, value in self.props.items():
                result += f' {key}="{value}"'            
        return result
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        result = ""
        if self.props is not None:
#            prop_html = self.props_to_html()
            result += f"<{self.tag}{self.props_to_html()}>{self.value}"
        else:
            result += f"<{self.tag}>{self.value}"
        result += f"</{self.tag}>" 
        return result 