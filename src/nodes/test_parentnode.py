from test_utils import TestRunner
from nodes.parentnode import ParentNode
from nodes.leafnode import LeafNode

class TestParentNode(TestRunner):
    def setUp(self):
        # Common test elements
        self.leaf_1 = LeafNode("p", "Leaf 1")
        self.leaf_2 = LeafNode("p", "Leaf 2")
        self.basic_props = {"class": "parent", "id": "this-parent"}
        self.button_props = {"class": "btn", "type": "button"}
        self.parent_fields = ["tag", "children", "props"]

    invalid_children_cases = [
        {
            "name": "None children",
            "tag": "div",
            "children": None,
            "expected_error": "A parent node must have children"
        },
        {
            "name": "Empty children list",
            "tag": "div",
            "children": [],
            "expected_error": "A parent node must have children"
        }
    ]

    invalid_tag_cases = [
        {
            "name": "None tag",
            "tag": None,
            "children": [LeafNode("div", "test")],
            "expected_error": "A parent node must have children"
        },
        {
            "name": "Empty tag",
            "tag": "",
            "children": [LeafNode("div", "test")],
            "expected_error": "A parent node must have children"
        }
    ]

    html_rendering_cases = [
        {
            "name": "Simple parent with two leaves",
            "setup": lambda self: ParentNode(
                "div", 
                [self.leaf_1, self.leaf_2], 
                props=self.basic_props
            ),
            "expected": '<div class="parent" id="this-parent"><p>Leaf 1</p><p>Leaf 2</p></div>'
        },
        {
            "name": "Nested structure",
            "setup": lambda self: ParentNode("section", [
                self.leaf_1,
                self.leaf_2,
                ParentNode("section", [
                    self.leaf_1,
                    ParentNode("div", [self.leaf_1, self.leaf_2], props=self.basic_props)
                ], props=self.basic_props)
            ], props=self.basic_props),
            "expected": '<section class="parent" id="this-parent"><p>Leaf 1</p><p>Leaf 2</p><section class="parent" id="this-parent"><p>Leaf 1</p><div class="parent" id="this-parent"><p>Leaf 1</p><p>Leaf 2</p></div></section></section>'
        }
    ]

    equal_cases = [
        {
            "name": "Equal parent nodes",
            "make_node": lambda self: ParentNode(
                tag="button",
                children=[
                    LeafNode("button", "Test", props=self.button_props),
                    LeafNode("button", "Test", props=self.button_props)
                ],
                props=self.button_props
            ),
            "expected": True
        }
    ]

    not_equal_cases = [
        {
            "name": "unequal tag",
            "make_other": lambda self: ParentNode(
                tag="div",
                children=[
                    LeafNode("button", "Test", props=self.button_props),
                    LeafNode("button", "Test", props=self.button_props)
                ],
                props=self.button_props
            ),
        },
        {
            "name": "less children",
            "make_other": lambda self: ParentNode(
                tag="div",
                children=[
                    LeafNode("button", "Test", props=self.button_props),
                ],
                props=self.button_props
            ),
        },
        {
            "name": "different children",
            "make_other": lambda self: ParentNode(
                tag="div",
                children=[
                    LeafNode("button", "Test", props=self.button_props),
                    LeafNode("button", "TEST", props=self.button_props),
                ],
                props=self.button_props
            ),
        },
        {
            "name": "different children props",
            "make_other": lambda self: ParentNode(
                tag="div",
                children=[
                    LeafNode("button", "Test", props=self.button_props),
                    LeafNode("button", "Test", props={ "type": "submit" }),
                ],
                props=self.button_props
            ),
        },
        {
            "name": "different props",
            "make_other": lambda self: ParentNode(
                tag="div",
                children=[
                    LeafNode("button", "Test", props=self.button_props),
                    LeafNode("button", "Test", props=self.button_props),
                ],
                props=self.basic_props
            ),
        },
    ]

    def test_invalid_children(self):
        """Test cases where children are invalid"""
        for case in self.invalid_children_cases:
            with self.subTest(case["name"]):
                with self.assertRaises(ValueError) as context:
                    parent = ParentNode(case["tag"], case["children"])
                    parent.to_html()
                self.assertTrue(case["expected_error"])

    def test_invalid_tag(self):
        """Test cases where tag is invalid"""
        for case in self.invalid_tag_cases:
            with self.subTest(case["name"]):
                with self.assertRaises(ValueError) as context:
                    parent = ParentNode(case["tag"], case["children"])
                    parent.to_html()
                self.assertTrue(case["expected_error"])

    def test_to_html(self):
        """Test HTML rendering for various node structures"""
        for case in self.html_rendering_cases:
            with self.subTest(case["name"]):
                node = case["setup"](self)
                self.assertEqual(node.to_html(), case["expected"])

    def test_eq(self):
         for case in self.not_equal_cases:
            with self.subTest(case["name"]):
                node = self.equal_cases[0]["make_node"](self)
                other = case["make_other"](self)
                self.assertNotEqual(node, other)
