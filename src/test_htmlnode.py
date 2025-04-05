import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


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

if __name__ == "__main__":
    unittest.main()