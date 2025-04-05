import unittest

from src.extract import extract_markdown_images, extract_markdown_link


class TestExtract(unittest.TestCase):
    def test_image_extractor_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertEqual(
        images,
        [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        )

    def test_image_extractor_image_link(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertEqual(
            images,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif")
            ]
        )

    def test_link_extractor_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_link(text)
        self.assertEqual(
        links,
        [
            ("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        )

    def test_link_extractor_link_image(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_link(text)
        self.assertEqual(
            links,
            [
                ("to boot dev", "https://www.boot.dev")
            ]
        )

