import unittest

from src.split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
from src.textnode import TextType, TextNode


class TestSplitNodeDelimiters(unittest.TestCase):
    def test_split_node_delimiters_text_one(self):
        node1 = TextNode('`test`', TextType.TEXT)
        split_nodes = split_nodes_delimiter([node1], "`", TextType.CODE)
        self.assertEqual(split_nodes, [TextNode('test', TextType.CODE)])


    def test_split_node_delimiters_text_many(self):
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

    def test_split_node_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_node_image_with_link(self):
        node = TextNode(
            "Check out this ![image](https://example.com/img.jpg) and this [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("Check out this ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
                TextNode(" and this [link](https://example.com)", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_split_node_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_node_link_with_image(self):
        node = TextNode(
            "Check out this ![image](https://example.com/img.jpg) and this [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Check out this ![image](https://example.com/img.jpg) and this ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com")
            ],
            new_nodes,
        )
