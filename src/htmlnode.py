from src.blocks import split_markdown_to_blocks, TypeBlock, block_to_block_type
from src.split_nodes import text_to_textnodes
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
        if self.tag is None:
            return self.value or ""

        if self.children is None or len(self.children) == 0:
            return f"<{self.tag}></{self.tag}>"

        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        if self.value:
            return f"<{self.tag}>{self.value}{children_html}</{self.tag}>"
        else:
            return f"<{self.tag}>{children_html}</{self.tag}>"

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

def determine_heading_level(header_text: str):
    count = 0
    for c in header_text:
        if c == "#":
            count += 1
        else:
            break
    return count

def markdown_to_html_node(markdown):
    blocks = split_markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == TypeBlock.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == TypeBlock.HEADING:
        return heading_to_html_node(block)
    if block_type == TypeBlock.CODE:
        return code_to_html_node(block)
    if block_type == TypeBlock.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == TypeBlock.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == TypeBlock.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
