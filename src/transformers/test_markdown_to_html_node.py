from test_utils import TestRunner
from nodes.textnode import TextNode, TextType
from nodes.leafnode import LeafNode
from nodes.parentnode import ParentNode
from transformers.markdown_to_html_node import markdown_to_html_node, block_string_to_html_nodes, make_heading_node, make_code_node, make_quote_node, make_list_node

class TestMakeHeadingAndQuoteNodes(TestRunner):
    heading_cases = [
        { 
            "name": "h1 leaf", 
            "text": "# Major heading",
            "expected": {
                "tag": "h1", 
                "children": ["Major heading"]
            }
        },
        { 
            "name": "h3 parent",
            "text": "### I contain `code` and **boldness**",
            "expected": {
                "tag": "h3",
                "children": [
                    LeafNode(tag=None, value="I contain "),
                    LeafNode(tag="code", value="code"),
                    LeafNode(tag=None, value=" and "),
                    LeafNode(tag="b", value="boldness"),
                ]
            }
        },
        { 
            "name": "h1 leaf", 
            "text": "# Major heading",
            "expected": {
                "tag": "h1", 
                "children": ["Major heading"]
            }
        },
        { 
            "name": "h3 parent with image and link",
            "text": "### *italic* and ![alt](foo.png) and [goto](#somewhere).",
            "expected": {
                "tag": "h3",
                "children": [
                    LeafNode(tag="i", value="italic"),
                    LeafNode(tag=None, value=" and "),
                    LeafNode(tag="img", value="", 
                             props={ "src": "foo.png", "alt": "alt" }),
                    LeafNode(tag=None, value=" and "),
                    LeafNode(tag="a", value="goto", 
                             props={ "href": "#somewhere" }),
                    LeafNode(tag=None, value="."),
                ]
            }
        },
    ]

    def test_heading_cases(self):
         for case in self.heading_cases:
            with self.subTest(case["name"]):
                actual = make_heading_node(case["text"])
                expected_children = case["expected"]["children"]
                if len(expected_children) == 1:
                    expected = LeafNode(case["expected"]["tag"], expected_children[0])
                    self.assertEqual(actual, expected)
                else:
                    expected = ParentNode(case["expected"]["tag"], expected_children)
                    self.assertEqual(actual, expected)
                    self.assertEqual(repr(actual), repr(expected))
                    self.assertEqual(len(expected_children), len(list(actual.children)))
                    
class TestMakeCodeNode(TestRunner):
    cases = [
        {
            "name": "one line",
            "text": "```print('foobar')```",
            "expected_params": {
                "tag": "pre",
                "children": [LeafNode("code", "print('foobar')")]
            }
        },
        {
            "name": "multiple lines",
            "text": "```\nprint('foobar')\nprint('foobar again')\n```",
            "expected_params": {
                "tag": "pre",
                "children": [LeafNode("code", "\nprint('foobar')\nprint('foobar again')\n")]
            }
        }
    ]

    def test_cases(self):
        for case in self.cases:
            with self.subTest(case["name"]):
                actual = make_code_node(case["text"])
                expected = ParentNode(**case["expected_params"])
                self.assertEqual(actual, expected)

class TestMakeQuoteListAndParagraphNodes(TestRunner):
    quote_cases = [
        { 
            "name": "quote with only normal text", 
            "text": "> and I quote",
            "expected": {
                "tag": "blockquote", 
                "children": ["and I quote"]
            }
        },
        { 
            "name": "quote with all the children",
            "text": "> *italic* and ![alt](foo.png) and [goto](#somewhere).",
            "expected": {
                "tag": "blockquote",
                "children": [
                    LeafNode(tag="i", value="italic"),
                    LeafNode(tag=None, value=" and "),
                    LeafNode(tag="img", value="", 
                             props={ "src": "foo.png", "alt": "alt" }),
                    LeafNode(tag=None, value=" and "),
                    LeafNode(tag="a", value="goto", 
                             props={ "href": "#somewhere" }),
                    LeafNode(tag=None, value="."),
                ]
            }
        },
    ]

    def test_quote_cases(self):
         for case in self.quote_cases:
            with self.subTest(case["name"]):
                actual = make_quote_node(case["text"])
                expected_children = case["expected"]["children"]
                if len(expected_children) == 1:
                    expected = LeafNode(case["expected"]["tag"], expected_children[0])
                    self.assertEqual(actual, expected)
                else:
                    expected = ParentNode(case["expected"]["tag"], expected_children)
                    self.assertEqual(actual, expected)
                    self.assertEqual(repr(actual), repr(expected))
                    self.assertEqual(len(expected_children), len(list(actual.children)))

    list_cases = [
        { 
            "name": "unordered with one item",
            "text": "* one list item",
            "expected": {
                "tag": "ul",
                "children": [LeafNode("li", "one list item")]
            }
        },
        
        { 
            "name": "ordered with one item",
            "text": "1. one ordered list item",
            "expected": {
                "tag": "ol", 
                "children": [LeafNode("li", "one ordered list item")]
            }
        },

        { 
            "name": "unordered with plain text",
            "text": "* a one\n* and a two\n* and a three",
            "expected": {
                "tag": "ul",
                "children": [
                    LeafNode(tag="li", value="a one"),
                    LeafNode(tag="li", value="and a two"),
                    LeafNode(tag="li", value="and a three"),
                ]
            }
        },
        { 
            "name": "unordered with dashes",
            "text": "- a one\n- and a two\n- and a three",
            "expected": {
                "tag": "ul",
                "children": [
                    LeafNode(tag="li", value="a one"),
                    LeafNode(tag="li", value="and a two"),
                    LeafNode(tag="li", value="and a three"),
                ]
            }
        },
        
         { 
            "name": "unordered with various content",
            "text": "* line 1 *italic* and ![alt](foo.png)\n* line 2 [goto](#somewhere)\n* line 3 **bold** `print('foobar')`",
            "expected": {
                "tag": "ol",
                "children": [
                    ParentNode("li", 
                               children=[LeafNode(None, "line 1 "), 
                                         LeafNode(tag="i", value="italic"), LeafNode(tag=None, value=" and "),
                                         LeafNode(tag="img", value="", props={ "src": "foo.png", "alt": "alt" })]),
                    ParentNode("li", 
                               children=[LeafNode(tag=None, value="line 2 "), 
                                         LeafNode(tag="a", value="goto", 
                                            props={ "href": "#somewhere" })]),
                    ParentNode("li", 
                               children=[LeafNode(None, "line 3 "),
                                         LeafNode("b", "bold"),
                                         LeafNode(None, " "),
                                         LeafNode("code", "print('foobar')")])
                ]
            }
        },
    ]    

    def test_list_cases(self):
         for case in self.list_cases:
            with self.subTest(case["name"]):
                actual = make_list_node(case["text"], case["expected"]["tag"])
                expected_children = case["expected"]["children"]
                expected = ParentNode(case["expected"]["tag"],
                                        children=expected_children)
                self.assertEqual(actual, expected)
                self.assertEqual(repr(actual), repr(expected))
                self.assertEqual(len(list(actual.children)), len(expected_children))
