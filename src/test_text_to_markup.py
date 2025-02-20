import unittest
from text_to_markup import text_to_html
from textnode import TextNode, TextType
from leafnode import LeafNode

class TestTextToMarkup(unittest.TestCase):
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
