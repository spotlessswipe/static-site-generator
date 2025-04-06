import re

from src.extract import extract_markdown_images, extract_markdown_links
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


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        current_text = node.text

        while True:
            images = extract_markdown_images(current_text)
            if images:
                image_info = images[0]
            else:
                if current_text:
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
                break

            # Unpack the image info
            image_alt, image_url = image_info

            # before after
            sections = current_text.split(f"![{image_alt}]({image_url})", 1)

            # Add text before the image if not empty
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))

            current_text = sections[1]

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        current_text = node.text

        while True:
            links = extract_markdown_links(current_text)
            if links:
                link_info = links[0]
            else:
                if current_text:
                    new_nodes.append(TextNode(current_text, TextType.TEXT))
                break

            # Unpack the link info
            link_alt, link_url = link_info

            # before after
            sections = current_text.split(f"[{link_alt}]({link_url})", 1)

            # Add text before the link if not empty
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))

            current_text = sections[1]

    return new_nodes

def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)

    return text_nodes

def markdown_to_blocks(markdown: str):
    blocks = markdown.split('\n\n')

    new_blocks = []
    for block in blocks:
        cleaned_text = block.strip()
        if cleaned_text:
            new_blocks.append(cleaned_text)

    return new_blocks