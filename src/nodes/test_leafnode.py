import unittest
from nodes.leafnode import LeafNode


equality_test_node_params = {
    "tag": "p",
    "value": "text",
    "props": {
        "class": "foo foo_bar_baz",
        "id": "this-node"
    }
}

class TestLeafNode(unittest.TestCase):
    leaf_test_cases = [
        {
            "name": "button with props",
            "node_params": {
                "tag": "button",
                "value": "Test",
                "props": {"class": "btn", "type": "button"}
            },
            "expected_html": '<button class="btn" type="button">Test</button>',
            "expected_str": '<button class="btn" type="button">\n  Test\n</button>'
        },
        {
            "name": "text only",
            "node_params": {
                "tag": None,
                "value": "Test"
            },
            "expected_html": "Test",
            "expected_str": "Test"
        }
    ]

    text_only_cases = [
        {
            "name": "simple text",
            "node_params": {
                "tag": None,
                "value": "Hello world"
            },
            "expected_str": "Hello world",
            "expected_repr": "Hello world",
            "expected_html": "Hello world"
        },
        {
            "name": "text with special chars",
            "node_params": {
                "tag": None,
                "value": "Hello & goodbye"
            },
            "expected_str": "Hello & goodbye",
            "expected_repr": "Hello & goodbye",
            "expected_html": "Hello & goodbye"
        }
    ]


    equality_cases = [
        {
            "name": "equal with tag and props",
            "node_params": equality_test_node_params,
            "expected_equal": True
        },
        {
            "name": "equal without tag",
            "node_params": {
                "tag": None,
                "value": "text",
            },
            "expected_equal": True
        }
    ]

    def test_with_children(self):
        with self.assertRaises(TypeError) as context:
            child = LeafNode("div", "child")
            LeafNode("p", "foobar", children=[child])
        self.assertTrue("got an unexpected keyword argument 'children'" in str(context.exception))

    def test_to_html_with_bad_value(self):
        # If the value argument is omitted, an TypeError is raised
        with self.assertRaises(TypeError) as context:
            LeafNode("p")
        self.assertTrue("missing 1 required positional argument: 'value'" in str(context.exception))
        
        # If value not a string when to_html is called a ValueError is raised.
        invalid_cases = [
            ("None value", LeafNode("p", None)),
            ("Dict value", LeafNode("p", {"key": "val"})),
            ("List value", LeafNode("p", ["List item"]))
        ]
        
        for case_name, node in invalid_cases:
            with self.subTest(case_name):
                with self.assertRaises(ValueError) as context:
                    node.to_html()
                self.assertTrue("A leaf must have a value" in str(context.exception))

    def test_leaf_rendering(self):
        for case in self.leaf_test_cases:
            with self.subTest(case["name"]):
                node = LeafNode(**case["node_params"])
                self.assertEqual(node.to_html(), case["expected_html"])
                self.assertEqual(str(node), case["expected_str"])

    def test_text_only_nodes(self):
        for case in self.text_only_cases:
            with self.subTest(case["name"]):
                node = LeafNode(**case["node_params"])
                self.assertEqual(str(node), case["expected_str"])
                self.assertEqual(repr(node), case["expected_repr"])
                self.assertEqual(node.to_html(), case["expected_html"])

    def test_equality(self):
        for case in self.equality_cases:
            with self.subTest(case["name"]):
                node = LeafNode(**case["node_params"])
                other = LeafNode(**case["node_params"])
                self.assertEqual(node == other, case["expected_equal"])

    def test_inequality(self):
        node = LeafNode(**equality_test_node_params)
        other_params = equality_test_node_params.copy()

        props = { "tag": "different", "value": "different", "props": { "different": True} }

        for prop in props:
            other_params[prop] = props[prop]
            self.assertNotEqual(node, LeafNode(**other_params))

            other_params[prop] = None
            self.assertNotEqual(node, LeafNode(**other_params))

            other_params[prop] = equality_test_node_params[prop]