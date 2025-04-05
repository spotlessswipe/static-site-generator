import re

from src.textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []

    escaped_delimiter = re.escape(delimiter) # in case special sign
    pattern = f"{escaped_delimiter}(.*?){escaped_delimiter}"

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = list(re.finditer(pattern, node.text))

        if not matches:
            new_nodes.append(node)
            continue

        # Track where we are in the string
        last_end = 0
        for match in matches:
            if match.start() > last_end:
                before_text = node.text[last_end:match.start()]
                new_nodes.append(TextNode(before_text, TextType.TEXT))

            matched_text = match.group(1)
            new_nodes.append(TextNode(matched_text, text_type))

            last_end = match.end()

        # Text after the last match
        if last_end < len(node.text):
            after_text = node.text[last_end:]
            new_nodes.append(TextNode(after_text, TextType.TEXT))

    return new_nodes


