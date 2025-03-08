from test_utils import TestRunner
from nodes.leafnode import LeafNode
from nodes.voidnode import VoidNode
from nodes.parentnode import ParentNode
from transformers.markdown_to_html_node import markdown_to_html_node, block_string_to_html_nodes, make_heading_node, make_code_node, make_quote_node, make_list_node

class TestMarkdownToHTMLNode(TestRunner):
    cases = [
        {
            "name": "image in a block alone",
            "text": """# Tolkien Fan Club

                    ![JRR Tolkien sitting](/images/tolkien.png)
            """,
            "expected": {
                "tag": "div",
                "children": [LeafNode("h1", "Tolkien Fan Club"),
                             VoidNode("img", value="",
                                      props={ "src": "/images/tolkien.png",
                                              "alt": "JRR Tolkien sitting"}),
                ],
            }
        },
        {
            "name": "image and link in a block alone",
            "text": """# Tolkien Fan Club

                    [goto](http://tolkien.com)
            """,
            "expected": {
                "tag": "div",
                "children": [LeafNode("h1", "Tolkien Fan Club"),
                             LeafNode("a", value="goto",
                                      props={ "href": "http://tolkien.com"}),
                ],
            }
        },

        {
            "name": "full example",
            "text": "# Musings on Unit Testing\n\nUnit testing your code is a *great* way to build confidence and make friends. Here are some tips.\n\n## Useful tips\n\n1. Talk about unit testing when you are at a party\n2. To impress a date, mention your project's test coverage\n\n## The kids like it too\n\nTry these **kid-friendly** activities:\n\n- write a program to distribute chores among siblings and require each sibling to write a share of the unit tests\n- every day is 'take a child to work' day if you make your child watch you as you write your unit tests\n\n## Random code example\n\n```python\nprint('Hello, world!')\n```\n\n## Conclusion\n\nI leave you with some inspiring quotes:\n\n> Unit testing is next to Godliness. -- unknown author\n\n> On the 6th day, God unit tested. -- unknown author",
            "expected": {
                "tag": "div",
                "children": [
                    LeafNode("h1", "Musings on Unit Testing"),
                    ParentNode("p", children=[
                        LeafNode(None, "Unit testing your code is a "),
                        LeafNode("i", "great"),
                        LeafNode(None, " way to build confidence and make friends. Here are some tips.")
                    ]),
                    LeafNode("h2", "Useful tips"),
                    ParentNode("ol", children=[
                        LeafNode("li", "Talk about unit testing when you are at a party"),
                        LeafNode("li", "To impress a date, mention your project's test coverage")
                    ]),
                    LeafNode("h2", "The kids like it too"),
                    ParentNode("p", children=[
                        LeafNode(None, "Try these "),
                        LeafNode("b", "kid-friendly"),
                        LeafNode(None, " activities:")
                    ]),
                    ParentNode("ul", children=[
                        LeafNode("li", "write a program to distribute chores among siblings and require each sibling to write a share of the unit tests"),
                        LeafNode("li", "every day is 'take a child to work' day if you make your child watch you as you write your unit tests")
                    ]),
                    LeafNode("h2", "Random code example"),
                    ParentNode("pre", children=[LeafNode("code", "python\nprint('Hello, world!')\n")]),
                    LeafNode("h2", "Conclusion"),
                    LeafNode("p", "I leave you with some inspiring quotes:"),
                    LeafNode("blockquote", "Unit testing is next to Godliness. -- unknown author"),
                    LeafNode("blockquote", "On the 6th day, God unit tested. -- unknown author")
                ]
            }
        }
    ]

    def test_cases(self):
         for case in self.cases:
            with self.subTest(case["name"]):
                actual = markdown_to_html_node(case["text"])
                expected_children = case["expected"]["children"]
                expected = ParentNode(case["expected"]["tag"],
                                        children=expected_children)
                self.assertEqual(actual, expected)
                self.assertEqual(repr(actual), repr(expected))
                self.assertEqual(len(list(actual.children)), len(expected_children))


class TestBlockStringToHTMLNodes(TestRunner):
    cases = [
       {
            "name": "h1",
            "text": "# Test",
            "expected_tag": "h1",
       },
       {
            "name": "h1 multiline",
            "text": "# Test\n123",
            "expected_tag": "h1",
       },
       {
            "name": "h3",
            "text": "### Test",
            "expected_tag": "h3",
       },

       {
            "name": "p (no space == not heading)",
            "text": "#Test",
            "expected_tag": "p",
       },
       {
            "name": "p (7 #s == not heading)",
            "text": "####### Test",
            "expected_tag": "p",
       },

       { 
            "name": "code",
            "text": "```print('foo')```",
            "expected_tag": "pre",
       },     
       {
            "name": "code multiline",
            "text": "```print('foo')\nprint('bar')```",
            "expected_tag": "pre",
       },
       {
            "name": "p (less than 3 backticks == not code block)",
            "text": "``print('foo')``",
            "expected_tag": "p",
       },

       { 
            "name": "quote",
            "text": "> Quote",
            "expected_tag": "blockquote",
       },
       {
            "name": "quote multiline",
            "text": "> Quote\n> end quote",
            "expected_tag": "blockquote",
       },
       {
            "name": "p - (not quote multiline)",
            "text": "> Quote\n end quote",
            "expected_tag": "p",
       },
       {
            "name": "p - (not quote missing space)",
            "text": ">Quote",
            "expected_tag": "p",
       },

       {
            "name": "ul with one item (asterisk)",
            "text": "* Test",
            "expected_tag": "ul",
       },
       {
            "name": "ul with one item (dash)",
            "text": "- Test",
            "expected_tag": "ul",
       },
       {
            "name": "ul with multiple items (asterisk)",
            "text": "* Testing\n* Testing",
            "expected_tag": "ul",
       },

       {
            "name": "p (missing space == not ul)",
            "text": "*Testing\n* Testing",
            "expected_tag": "p",
       },

       {
            "name": "ol",
            "text": "1. abc\n2. def",
            "expected_tag": "ol",
       },      
       {
            "name": "p - (missing space == not ol)",
            "text": "1.abc\n2. def",
            "expected_tag": "p",
       },
       {
            "name": "p - (missing number == not ol)",
            "text": "1.abc\n3. xyz",
            "expected_tag": "p",
       },
       {
            "name": "p - (missing dot == not ol)",
            "text": "1 abc\n2. def",
            "expected_tag": "p",
       },
       {
            "name": "p - (missing 1. == not ol)",
            "text": "2. def\n3. xyz",
            "expected_tag": "p",
       },
    ]

    def test_cases(self):
        for case in self.cases:
            with self.subTest(case["name"]):
                actual = block_string_to_html_nodes(case["text"])
                self.assertEqual(actual.tag, case["expected_tag"])

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
                    VoidNode(tag="img", value="",
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
                    VoidNode(tag="img", value="",
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
                                         VoidNode(tag="img", value="", props={ "src": "foo.png", "alt": "alt" })]),
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

    def test_cases(self):
        for case in self.list_cases:
            with self.subTest(case["name"]):
                actual = make_list_node(case["text"], case["expected"]["tag"])
                expected_children = case["expected"]["children"]
                expected = ParentNode(case["expected"]["tag"],
                                        children=expected_children)
                self.assertEqual(actual, expected)
                self.assertEqual(repr(actual), repr(expected))
                self.assertEqual(len(list(actual.children)), len(expected_children))
