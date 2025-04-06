from enum import Enum


class TypeBlock(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def block_to_block_type(markdown_text_block: str):
    if check_if_markdown_heading(markdown_text_block):
        return TypeBlock.HEADING
    elif check_if_markdown_code(markdown_text_block):
        return  TypeBlock.CODE
    elif check_if_markdown_quote(markdown_text_block):
        return TypeBlock.QUOTE
    elif check_if_markdown_unordered_list(markdown_text_block):
        return TypeBlock.UNORDERED_LIST
    elif check_if_markdown_ordered_list(markdown_text_block):
        return TypeBlock.ORDERED_LIST
    else:
        return TypeBlock.PARAGRAPH


def check_if_markdown_heading(markdown: str):
    if markdown:
        hash_count = 0
        for character in markdown:
            if character == '#':
                hash_count += 1
            elif character == ' ' and hash_count <=7:
                return True
            else:
                return False


def check_if_markdown_code(markdown: str):
    return True if (
        len(markdown) > 6 and
        markdown[0:3] == '```' and
        markdown[-3:] == '```'
    ) else False


def check_if_markdown_quote(markdown: str):
    lines = markdown.split('\n')
    for i, line in enumerate(lines):
        if line[0] != '>':
            return False
        elif line[0] == '>' and i != len(lines)-1:
            continue
        elif line[0] == '>' and i == len(lines)-1:
            return True


def check_if_markdown_unordered_list(markdown: str):
    lines = markdown.split('\n')
    for i, line in enumerate(lines):
        if line[:2] != '- ':
            return False
        elif line[:2] == '- ' and i != len(lines)-1:
            continue
        elif line[:2] == '- ' and i == len(lines)-1:
            return True


def check_if_markdown_ordered_list(markdown: str):
    lines = markdown.split('\n')
    for i, line in enumerate(lines):
        if line[:3] != f'{i+1}. ':
            return False
        elif line[:3] == f'{i+1}. ' and i != len(lines)-1:
            continue
        elif line[:3] == f'{i+1}. ' and i == len(lines)-1:
            return True


def split_markdown_to_blocks(markdown: str):
    blocks = markdown.split('\n\n')

    new_blocks = []
    for block in blocks:
        cleaned_text = block.strip()
        if cleaned_text:
            new_blocks.append(cleaned_text)

    return new_blocks

