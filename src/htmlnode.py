class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None: return ""

        properties = ""
        for key in self.props:
            properties += f'{key}="{self.props[key]}" '
        return properties.rstrip()

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"



class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props = None)

    def to_html(self):
        if self.tag == None or self.tag == "" : raise ValueError
        if self.children == None: raise ValueError
        html = f"<{self.tag}>"
        for child in self.children:
            html += child.to_html()
        return html + f"</{self.tag}>"
    

    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None or self.value == "": raise ValueError
        if self.tag == "" or self.tag == None: return self.value

        if self.props != None:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"