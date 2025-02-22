import unittest
from text_to_markup import text_to_html, split_node, split_nodes_by_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType
from leafnode import LeafNode

delimiters = [
    {"char": "**", "text_type":  TextType.BOLD},
    {"char": "*", "text_type": TextType.ITALIC},
    {"char": "`", "text_type": TextType.CODE}
]

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

class TestExtractMarkdownImages(unittest.TestCase):
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

class TestExtractMarkdownLinks(unittest.TestCase):
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
