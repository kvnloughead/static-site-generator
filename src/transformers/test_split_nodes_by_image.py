from test_utils import TestRunner
from transformers.split_nodes_by_image import split_nodes_by_image
from nodes.textnode import TextNode, TextType
from nodes.leafnode import LeafNode

class TestSplitNode(TestRunner):
    simple_cases = [
        {
            "name": "simple case",
            "old_nodes": [
                LeafNode("p", "text"), TextNode("left ![alt](https://example.png) right", TextType.NORMAL), LeafNode("p", "text")
            ],
            "expected": [
                LeafNode("p", "text"),
                TextNode("left ", TextType.NORMAL),
                TextNode("alt", TextType.IMAGE, url="https://example.png"),
                TextNode(" right", TextType.NORMAL),
                LeafNode("p", "text")
            ],
                
        },
        {
            "name": "multiple images",
            "old_nodes": [
                LeafNode("p", "text"), TextNode("left ![alt](https://example.png) right", TextType.NORMAL), LeafNode("p", "text"), TextNode("left ![alt](https://example.png) right", TextType.NORMAL), LeafNode("p", "text"), LeafNode("p", "text")
            ],
            "expected": [
                LeafNode("p", "text"),
                TextNode("left ", TextType.NORMAL),
                TextNode("alt", TextType.IMAGE, url="https://example.png"),
                TextNode(" right", TextType.NORMAL),
                LeafNode("p", "text"),
                TextNode("left ", TextType.NORMAL),
                TextNode("alt", TextType.IMAGE, url="https://example.png"),
                TextNode(" right", TextType.NORMAL),
                LeafNode("p", "text"),
                LeafNode("p", "text")
            ],
                
        },
        {
            "name": "empty slots",
            "old_nodes": [
                TextNode("left ![alt](https://example.png) right", TextType.NORMAL), TextNode("left ![alt](https://example.png) right", TextType.NORMAL)
            ],
            "expected": [
                TextNode("left ", TextType.NORMAL),
                TextNode("alt", TextType.IMAGE, url="https://example.png"),
                TextNode(" right", TextType.NORMAL),
                TextNode("left ", TextType.NORMAL),
                TextNode("alt", TextType.IMAGE, url="https://example.png"),
                TextNode(" right", TextType.NORMAL),
            ],     
        },
        {
            "name": "multiple images in text node",
            "old_nodes": [
                TextNode("left ![alt](https://example.png) middle ![alt](https://example.png) right", TextType.NORMAL)
            ],
            "expected": [
                TextNode("left ", TextType.NORMAL),
                TextNode("alt", TextType.IMAGE, url="https://example.png"),
                TextNode(" middle ", TextType.NORMAL),
                TextNode("alt", TextType.IMAGE, url="https://example.png"),
                TextNode(" right", TextType.NORMAL),
            ],     
        },
        {
            "name": "no images in text node",
            "old_nodes": [
                TextNode("no images", TextType.NORMAL)
            ],
            "expected": [
                TextNode("no images", TextType.NORMAL),
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
                actual = split_nodes_by_image(case["old_nodes"])
                self.assertEqual(actual, case["expected"])