import unittest
from transformers.split_nodes_by_link import split_nodes_by_link
from nodes.textnode import TextNode, TextType
from nodes.leafnode import LeafNode

class TestSplitNode(unittest.TestCase):
    simple_cases = [
        {
            "name": "simple case",
            "old_nodes": [
                LeafNode("p", "text"), TextNode("left [here](https://example.com) right", TextType.NORMAL), LeafNode("p", "text")
            ],
            "expected": [
                LeafNode("p", "text"),
                TextNode("left ", TextType.NORMAL),
                TextNode("here", TextType.LINK, url="https://example.com"),
                TextNode(" right", TextType.NORMAL),
                LeafNode("p", "text")
            ],
                
        },
        {
            "name": "multiple links",
            "old_nodes": [
                LeafNode("p", "text"), TextNode("left [link text](https://example.com) right", TextType.NORMAL), LeafNode("p", "text"), TextNode("left [link text](https://example.com) right", TextType.NORMAL), LeafNode("p", "text"), LeafNode("p", "text")
            ],
            "expected": [
                LeafNode("p", "text"),
                TextNode("left ", TextType.NORMAL),
                TextNode("link text", TextType.LINK, url="https://example.com"),
                TextNode(" right", TextType.NORMAL),
                LeafNode("p", "text"),
                TextNode("left ", TextType.NORMAL),
                TextNode("link text", TextType.LINK, url="https://example.com"),
                TextNode(" right", TextType.NORMAL),
                LeafNode("p", "text"),
                LeafNode("p", "text")
            ],
                
        },
        {
            "name": "empty slots",
            "old_nodes": [
                TextNode("left [link text](https://example.com) right", TextType.NORMAL), TextNode("left [link text](https://example.com) right", TextType.NORMAL)
            ],
            "expected": [
                TextNode("left ", TextType.NORMAL),
                TextNode("link text", TextType.LINK, url="https://example.com"),
                TextNode(" right", TextType.NORMAL),
                TextNode("left ", TextType.NORMAL),
                TextNode("link text", TextType.LINK, url="https://example.com"),
                TextNode(" right", TextType.NORMAL),
            ],     
        },
        {
            "name": "multiple links in text node",
            "old_nodes": [
                TextNode("left [link text](https://example.com) middle [link text](https://example.com) right", TextType.NORMAL)
            ],
            "expected": [
                TextNode("left ", TextType.NORMAL),
                TextNode("link text", TextType.LINK, url="https://example.com"),
                TextNode(" middle ", TextType.NORMAL),
                TextNode("link text", TextType.LINK, url="https://example.com"),
                TextNode(" right", TextType.NORMAL),
            ],     
        },
        {
            "name": "no links in text node",
            "old_nodes": [
                TextNode("no links", TextType.NORMAL)
            ],
            "expected": [
                TextNode("no links", TextType.NORMAL),
            ],     
        },
        {
            "name": "no nodes",
            "old_nodes": [],
            "expected": [],
        }

    ]

    def test_simple_cases(self):
           for case in self.simple_cases:
            with self.subTest(case["name"]):
                actual = split_nodes_by_link(case["old_nodes"])
                self.assertEqual(actual, case["expected"])