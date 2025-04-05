

class HTMLNode:
    def __init__(
            self,
            tag: str = None,
            value: str = None,
            children: list["HTMLNode"] = None,
            props: dict[str, str] = None
    ):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return "" if not self.props else "".join(f" {key}=\"{value}\"" for key, value in self.props.items())

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def __init__(
            self,
            tag: str,
            value: str,
            props: dict[str, str] = None
    ):
        super().__init__(tag, value, [], props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"