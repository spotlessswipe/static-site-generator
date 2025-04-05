import re


def extract_markdown_images(text: str):
    regex = r'!\[([^\[\]]*)\]\(([^\(\)]*)\)'
    matches = re.findall(regex, text)
    return matches

def extract_markdown_link(text: str):
    regex = r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)'
    matches = re.findall(regex, text)
    return matches