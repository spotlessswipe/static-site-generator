import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from src.textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):

    def test_init(self):
        node = HTMLNode(
            "p",
            'test',
            [],
            {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual("p", node.tag)
        self.assertEqual("test", node.value)
        self.assertEqual([], node.children)
        self.assertEqual({
                "href": "https://www.google.com",
                "target": "_blank",
            }, node.props)

    def test_props_to_html(self):
        node = HTMLNode(
        "p",
        'test',
        [],
        {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())

    def test_repr(self):
        node = HTMLNode(
        "p",
        'test',
        [],
        {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        printed = str(node)
        self.assertEqual("HTMLNode(p, test, [], {'href': 'https://www.google.com', 'target': '_blank'})", printed)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_link(self):
        node = LeafNode(
            "a",
            'link',
            {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank">link</a>'
            )

    def test_leaf_no_value_raises_error(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()

        with self.assertRaises(ValueError):
            node = LeafNode("p", "")
            node.to_html()

    def test_leaf_no_tag(self):
        node = LeafNode("", "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

class TestParentNode(unittest.TestCase):
    def test_parent_to_html_p(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parent_to_html_link(self):
        node = ParentNode(
            "a",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank"><b>Bold text</b>Normal text<i>italic text</i>Normal text</a>'
            )

    def test_parent_no_value_raises_error(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p", None)
            node.to_html()

        with self.assertRaises(ValueError):
            node = ParentNode("p", [])
            node.to_html()

        with self.assertRaises(ValueError):
            node = ParentNode(None, [LeafNode("b", "Bold text")])
            node.to_html()

        with self.assertRaises(ValueError):
            node = ParentNode("", [LeafNode("b", "Bold text")])
            node.to_html()

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, 'google.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {'href': 'google.com'})

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, 'google.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, {'src': 'google.com', 'alt': 'This is a text node'})

    def test_wrong_type_raise_exception(self):
        node = TextNode("This is a text node", TextType.TEXT, 'google.com')
        node.text_type = "invalid_type"

        with self.assertRaises(Exception):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()