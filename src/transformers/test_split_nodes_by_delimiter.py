import unittest
from transformers.split_nodes_by_delimiter import split_node, split_nodes_by_delimiter
from nodes.textnode import TextNode, TextType
from nodes.leafnode import LeafNode

delimiters = [
    {"char": "**", "text_type":  TextType.BOLD},
    {"char": "*", "text_type": TextType.ITALIC},
    {"char": "`", "text_type": TextType.CODE}
]

class TestSplitNode(unittest.TestCase):
    no_delimiter_cases = [
        {
            "name": "Without delimiter",
            "delimiter": "*",
            "text_type": TextType.BOLD,
            "node": TextNode("I am not bold", TextType.NORMAL),
            "expected": [
                TextNode("I am not bold", TextType.NORMAL),

            ],
        },                        
    ]

    one_delimiter_pair_cases = [
        {
            "name": "normal",
            "left": "ABC",
            "middle": "DEF",
            "right": "XYZ",
            "result_length": 3
        },
        {
            "name": "preserves whitespace",
            "left": " ABC ",
            "middle": " DEF ",
            "right": " XYZ ",
            "result_length": 3
        },
        {
            "name": "initial delimiter omits left",
            "left": "",
            "middle": "DEF",
            "right": "XYZ",
            "result_length": 2,
        },
        {
            "name": "empty left and right returns middle",
            "left": "",
            "middle": "DEF",
            "right": "",
            "result_length": 1
        },
        {
            "name": "empty middle returns all",
            "left": "ABC",
            "middle": "",
            "right": "XYZ",
            "result_length": 3 
        },
        {
            "name": "initial and final whitespace is preserved",
            "left": "  ",
            "middle": "DEF",
            "right": "  ",
            "result_length": 3 
        },
        {
            "name": "all empty returns only the middle node",
            "left": "",
            "middle": "",
            "right": "",
            "result_length": 1
        },
        {
            "name": "all whitespace returns three nodes",
            "left": " ",
            "middle": " ",
            "right": " ",
            "result_length": 3
        },
    ]                              

    def test_no_delimiter_cases(self):
        for case in self.no_delimiter_cases:
            with self.subTest(case["name"]):
                result = split_node(case["node"], case["delimiter"], case["text_type"])
                print("\nExpected:")
                for node in case["expected"]:
                    print(f"Text: {node.text}, Type: {node.text_type}, URL: {node.url}")
                print("\nActual:")
                for node in result:
                    print(f"Text: {node.text}, Type: {node.text_type}, URL: {node.url}")
                self.assertEqual(result, case["expected"])

    def test_empty_node(self):
        node = TextNode("", TextType.NORMAL)
        self.assertEqual(split_node(node, "*", TextType.BOLD), [])

    def test_with_one_delimiter_pair(self):
        for case in self.one_delimiter_pair_cases:
            with self.subTest(case["name"]):
                for delimiter in delimiters:
                    left, mid, right = case["left"], case["middle"], case["right"]
                    d, type = delimiter["char"], delimiter["text_type"]
                    text = left + d + mid + d + right
                    node = TextNode(text, TextType.NORMAL)
                    actual = split_node(node, d, type)
                    
                    expected = []
                    if left != "":
                        expected.append(TextNode(left, TextType.NORMAL))
                    expected.append(TextNode(mid, type))
                    if right != "":
                        expected.append(TextNode(right, TextType.NORMAL))

                    self.assertEqual(actual, expected)
                    if "result_length" in case:
                        self.assertEqual(len(actual), case["result_length"])

    def test_missing_closing_delimiter(self):
        with self.assertRaises(Exception) as context:
            node = TextNode("This *is invalid markdown", TextType.NORMAL)
            split_node(node, "*", TextType.BOLD)
        self.assertTrue('Invalid markdown. No closing delimiter found, searching for "*".')

class TestSplitNodeByDelimiter(unittest.TestCase):
    simple_cases = [
        {
            "name": "simple case with match",
            "delimiter": "`",
            "text_type": TextType.CODE,
            "old_nodes": [
                LeafNode("p", "text"), TextNode("Text with a `code block` word", TextType.NORMAL), LeafNode("p", "text")
            ],
            "expected": [
                LeafNode("p", "text"),  
                TextNode("Text with a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.NORMAL), 
                LeafNode("p", "text")
            ]
        },
        {
            "name": "simple case without match",
            "delimiter": "*",
            "text_type": TextType.ITALIC,
            "old_nodes": [
                LeafNode("p", "text"), TextNode("Text with a `code block` word", TextType.NORMAL), LeafNode("p", "text")
            ],
            "expected": [
                LeafNode("p", "text"), TextNode("Text with a `code block` word", TextType.NORMAL), LeafNode("p", "text")
            ],
        },
        {
            "name": "multiple text nodes case",
            "delimiter": "**",
            "text_type": TextType.BOLD,
            "old_nodes": [
                 TextNode("Text with a **bold** word", TextType.NORMAL), TextNode("Normal text", TextType.NORMAL), TextNode("*all italic*", TextType.NORMAL)
            ],
            "expected": [TextNode("Text with a ", TextType.NORMAL),
                         TextNode("bold", TextType.BOLD),
                         TextNode(" word", TextType.NORMAL),
                         TextNode("Normal text", TextType.NORMAL),
                         TextNode("*all italic*", TextType.NORMAL),
            ]
        }
    ]

    def test_simple_cases(self):
        for case in self.simple_cases:
            with self.subTest(case["name"]):
                new_nodes = split_nodes_by_delimiter(
                    case["old_nodes"],
                    case["delimiter"],
                    case["text_type"])
                self.assertEqual(new_nodes, case["expected"])

    def test_missing_closing_delimiter(self):
        with self.assertRaises(Exception) as context:
            node = TextNode("This *is invalid markdown", TextType.NORMAL)
            split_nodes_by_delimiter(
                [TextNode("valid", TextType.NORMAL), node],
                "*",
                TextType.BOLD)
        self.assertTrue('Invalid markdown. No closing delimiter found, searching for "*".')
