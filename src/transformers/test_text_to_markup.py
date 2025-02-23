from test_utils import TestRunner
from transformers.text_to_markup import text_to_html, extract_markdown_images, extract_markdown_links
from nodes.textnode import TextNode, TextType
from nodes.leafnode import LeafNode

class TestTextToMarkup(TestRunner):
    simple_cases = [
        {
            "name": "normal text",
            "type": TextType.NORMAL,
            "tag": None
        },
        {
            "name": "bold text",
            "type": TextType.BOLD,
            "tag": "b"
        },
        {
            "name": "italic text",
            "type": TextType.ITALIC,
            "tag": "i"
        },
        {
            "name": "code formatted text",
            "type": TextType.CODE,
            "tag": "code"
        },
    ]

    image_cases = [
        {
            "name": "good image",
            "alt": "alt text",
            "tag": "img",
            "url": "https://example.png"
        },
        {
            "name": "no alt text",
            "alt": "",
            "tag": "img",
            "url": "https://example.png"
        },
        {
            "name": "no url",
            "alt": "alt text",
            "tag": "img",
            "url": ""
        },
    ]

    link_cases = [
        {
            "name": "good link",
            "tag": "a",
            "href": "https://example.com",
            "link_text": "link text"
        },
        {
            "name": "missing href",
            "tag": "a",
            "href": "",
            "link_text": "link text"
        },
        {
            "name": "missing text",
            "tag": "a",
            "href": "https://example.com",
            "link_text": ""
        }
    ]

    def test_bad_type(self):
        text_node = TextNode("bad type", "bad type")
        with self.assertRaises(ValueError) as context:
            text_to_html(text_node) 
        self.assertTrue("The text node's type must be an instance of textnode.TextType.")

    def test_simple_cases(self):
        for case in self.simple_cases:
            with self.subTest(case["name"]):
                leaf_node = LeafNode(case["tag"], case["name"])
                text_node = TextNode(case["name"], case["type"])
                leaf_from_text = text_to_html(text_node)
                self.assertEqual(leaf_node, leaf_from_text)

    def test_image_cases(self):
        for case in self.image_cases:
            with self.subTest(case["name"]):
                leaf_node = LeafNode(case["tag"], 
                                     "", 
                                     props={ "src": case["url"],
                                             "alt": case["alt"]})
                
                text_node = TextNode(case["alt"], 
                                     TextType.IMAGE, 
                                     url=case["url"])
                
                leaf_from_text = text_to_html(text_node)
                self.assertEqual(leaf_node, leaf_from_text)

    def test_link_cases(self):
         for case in self.link_cases:
            with self.subTest(case["name"]):
                leaf_node = LeafNode(case["tag"], 
                                     case["link_text"], 
                                     props={ "href": case["href"] })
                
                text_node = TextNode(case["link_text"], 
                                     TextType.LINK, 
                                     url=case["href"])
                
                leaf_from_text = text_to_html(text_node)
                self.assertEqual(leaf_node, leaf_from_text)


class TestExtractMarkdownImages(TestRunner):
    test_cases = [
        {
            "name": "with URL",
            "text": "Here is an image ![alt text](https://foo.png)",
            "expected": [("alt text", "https://foo.png")]
        },
        {
            "name": "with filepath",
            "text": "Here is an image ![alt text](../path/to/image.png)",
            "expected": [("alt text", "../path/to/image.png")]
        },
        {
            "name": "multiple images",
            "text": '![first](image.png) ![second](image.png)',
            "expected": [("first", "image.png"),
                         ("second", "image.png")]
        },
        {
            "name": "no images",
            "text": "Empty",
            "expected": []
        },
        {
            "name": "empty string",
            "text": "",
            "expected": []
        },
        {
            "name": "empty alt",
            "text": "Not accessible ![](image.png)",
            "expected": [("", "image.png")]
        },
        {
            "name": "empty URL",
            "text": "Not accessible ![alt]()",
            "expected": [("alt", "")]
        },
    ]

    def test_simple_cases(self):
         for case in self.test_cases:
            with self.subTest(case["name"]):
                images = extract_markdown_images(case["text"])
                self.assertEqual(images, case["expected"])

class TestExtractMarkdownLinks(TestRunner):
    test_cases = [
        {
            "name": "simple case",
            "text": "Here is a [link](https://example.com)",
            "expected": [("link", "https://example.com", "")]
        },
        {
            "name": "with title",
            "text": "Here is a [link](https://example.com \"title\")",
            "expected": [("link", "https://example.com", "title")]
        },
        {
            "name": "empty fields",
            "text": "Here is a []()",
            "expected": [("", "", "")]
        }
        
    ]

    def test_simple_cases(self):
         for case in self.test_cases:
            with self.subTest(case["name"]):
                links = extract_markdown_links(case["text"])
                self.assertEqual(links, case["expected"])
