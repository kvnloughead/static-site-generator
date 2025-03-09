import random
from test_utils import TestRunner
from nodes.htmlnode import HTMLNode

class TestHTMLNode(TestRunner):
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
            "expected": "</div>"
        },
    ]

    repr_cases = [
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
            "expected_repr": '<main><div><p class="text">Paragraph 1</p><p>Paragraph 2</p></div><div><p>Paragraph 3</p></div></main>'
        }
    ]

    def test_void_tag_not_using_voidnode(self):
        void_tag = random.choice(HTMLNode._self_closing_tags)
        msg = f"A {void_tag} tag is void and must be created as a VoidNode."
        self.assert_raises_exception(TypeError,
                                     msg,
                                     lambda: HTMLNode(tag=void_tag))

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
                result = node._get_closing_tag()
                self.assertEqual(result, case["expected"])

    def test_repr(self):
        for case in self.repr_cases:
            with self.subTest(case["name"]):
                node = case["setup"](self)
                self.assertEqual(repr(node), case["expected_repr"])