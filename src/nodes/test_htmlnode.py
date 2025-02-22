import unittest
from nodes.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def setUp(self):
        self.basic_props = {"class": "my-button", "type": "button"}
        self.basic_text = "Click me"

    props_test_cases = [
        {
            "name": "with props",
            "node_params": {
                "tag": "button",
                "value": "Click me",
                "props": {"class": "my-button", "type": "button"}
            },
            "expected": ' class="my-button" type="button"'
        },
        {
            "name": "without props",
            "node_params": {
                "tag": "button",
                "value": "Click me"
            },
            "expected": ""
        }
    ]

    opening_tag_cases = [
        {
            "name": "div with children",
            "setup": lambda self: HTMLNode(
                tag="div",
                children=[HTMLNode(tag="div"), HTMLNode(tag="div")]
            ),
            "expected": "<div>"
        },
        {
            "name": "text node",
            "setup": lambda self: HTMLNode(tag=None, value="Text"),
            "expected": "Text"
        }
    ]

    closing_tag_cases = [
        {
            "name": "simple div",
            "node": lambda: HTMLNode(tag="div"),
            "indent": None,
            "expected": "</div>"
        },
        {
            "name": "div with indent 0",
            "node": lambda: HTMLNode(tag="div", children=[HTMLNode(tag="div")]),
            "indent": 0,
            "expected": "\n</div>"
        },
        {
            "name": "div with indent 2",
            "node": lambda: HTMLNode(tag="div", children=[HTMLNode(tag="div")]),
            "indent": 2,
            "expected": "\n  </div>"
        }
    ]

    str_repr_cases = [
        {
            "name": "nested structure",
            "setup": lambda self: HTMLNode(
                tag="main",
                children=[
                    HTMLNode(
                        tag="div",
                        children=[
                            HTMLNode(tag="p", value="Paragraph 1", props={"class": "text"}),
                            HTMLNode(tag="p", value="Paragraph 2")
                        ]
                    ),
                    HTMLNode(
                        tag="div",
                        children=[
                            HTMLNode(tag="p", value="Paragraph 3")
                        ]
                    )
                ]
            ),
            "expected_str": '<main>\n  <div>\n    <p class="text">\n      Paragraph 1\n    </p>\n    <p>\n      Paragraph 2\n    </p>\n  </div>\n  <div>\n    <p>\n      Paragraph 3\n    </p>\n  </div>\n</main>',
            "expected_repr": '<main><div><p class="text">Paragraph 1</p><p>Paragraph 2</p></div><div><p>Paragraph 3</p></div></main>'
        }
    ]

    def test_bad_arguments(self):
        with self.assertRaises(TypeError) as context:
            HTMLNode()
        self.assertTrue("Must provide at least one of tag, value, or children")

    def test_props_to_html(self):
        for case in self.props_test_cases:
            with self.subTest(case["name"]):
                node = HTMLNode(**case["node_params"])
                self.assertEqual(node.props_to_html(), case["expected"])

    def test_get_opening_tag(self):
        for case in self.opening_tag_cases:
            with self.subTest(case["name"]):
                node = case["setup"](self)
                self.assertEqual(node._get_opening_tag(), case["expected"])

    def test_get_closing_tag(self):
        for case in self.closing_tag_cases:
            with self.subTest(case["name"]):
                node = case["node"]()
                result = node._get_closing_tag(case["indent"]) if case["indent"] is not None else node._get_closing_tag()
                self.assertEqual(result, case["expected"])

    def test_str_and_repr(self):
        for case in self.str_repr_cases:
            with self.subTest(case["name"]):
                node = case["setup"](self)
                self.assertEqual(str(node), case["expected_str"])
                self.assertEqual(repr(node), case["expected_repr"])