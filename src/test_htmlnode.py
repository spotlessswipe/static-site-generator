import unittest

from src.htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()