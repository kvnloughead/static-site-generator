import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def setUp(self):
        # Common test elements
        self.leaf_1 = LeafNode("p", "Leaf 1")
        self.leaf_2 = LeafNode("p", "Leaf 2")
        self.basic_props = {"class": "parent", "id": "this-parent"}
        self.button_props = {"class": "btn", "type": "button"}

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

    str_representation_cases = [
        {
            "name": "Button with nested buttons",
            "setup": lambda self: ParentNode(
                tag="button",
                children=[
                    LeafNode("button", "Test", props=self.button_props),
                    LeafNode("button", "Test", props=self.button_props)
                ],
                props=self.button_props
            ),
            "expected": '<button class="btn" type="button">\n  <button class="btn" type="button">\n    Test\n  </button>\n  <button class="btn" type="button">\n    Test\n  </button>\n</button>'
        }
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

    def test_str(self):
        """Test string representation of nodes"""
        for case in self.str_representation_cases:
            with self.subTest(case["name"]):
                node = case["setup"](self)
                self.assertEqual(str(node), case["expected"])

if __name__ == '__main__':
    unittest.main()