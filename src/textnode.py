from enum import Enum

class TextType(Enum):
    TEXT = "text"  # For normal text
    BOLD = "bold"  # For **bold text**
    ITALIC = "italic"  # For _italic text_
    CODE = "code"  # For `code text`
    LINK = "link"  # For [anchor text](url)
    IMAGE = "image"  # For ![alt text](url)

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
