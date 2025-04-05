from libxml2mod import children

from src.textnode import TextType, TextNode


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
            tag: str|None,
            value: str|None,
            props: dict[str, str] = None
    ):
        super().__init__(tag, value, [], props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(
            self,
            tag: str,
            children: list["HTMLNode"],
            props: dict[str, str] = None
    ):
        super().__init__(tag, '', children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("LeafParent must have a tag")
        if not self.children:
            raise ValueError("LeafParent must have a children")

        return f"<{self.tag}{self.props_to_html()}>{''.join(i.to_html() for i in self.children)}</{self.tag}>"

def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {'href': text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', "", {'src': text_node.url, 'alt': text_node.text})
        case _:
            raise Exception('TextNode wrong text type')