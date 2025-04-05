import unittest

from src.split_nodes_delimiter import split_nodes_delimiter
from src.textnode import TextType, TextNode


class TestSplitNodeDelimiters(unittest.TestCase):
    def test_split_note_delimiters_text_one(self):
        node1 = TextNode('`test`', TextType.TEXT)
        split_nodes = split_nodes_delimiter([node1], "`", TextType.CODE)
        self.assertEqual(split_nodes, [TextNode('test', TextType.CODE)])


    def test_split_note_delimiters_text_many(self):
        node1 = TextNode('**test**', TextType.TEXT)
        node2 = TextNode('abc abc', TextType.CODE)
        node3 = TextNode('**12hf** test1 **h** test2', TextType.TEXT)
        split_nodes = split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD)

        self.assertEqual(
            split_nodes,
            [
                TextNode('test', TextType.BOLD),
                TextNode('abc abc', TextType.CODE),
                TextNode('12hf', TextType.BOLD),
                TextNode(' test1 ', TextType.TEXT),
                TextNode('h', TextType.BOLD),
                TextNode(' test2', TextType.TEXT),
            ]
        )


