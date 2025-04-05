from htmlnode import HTMLNode
from textnode import TextNode, TextType


def main():
    text_node = TextNode('This is some anchor text', TextType.BOLD, 'https://www.boot.dev')
    print(text_node)
    html_node = HTMLNode(
        "p",
        'test',
        [],
        {
            "href": "https://www.google.com",
            "target": "_blank",
        }
    )
    print(html_node)

if __name__ == "__main__":
    main()