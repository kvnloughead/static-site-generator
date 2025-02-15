import unittest

from leafnode import LeafNode

class TestHTMLNode(unittest.TestCase):
    
    def test_with_children(self):
        with self.assertRaises(TypeError) as context:
            leaf_node = LeafNode("div")
            leaf_with_children = LeafNode("p", "foobar", children=[leaf_node])
            self.assertTrue("got an unexpected keyword argument 'children'")
        
    def test_to_html_without_value(self):
        # With None value
        with self.assertRaises(ValueError) as context:
            leaf_no_value = LeafNode("p", None)
            leaf_no_value.to_html()
            self.assertTrue("A leaf must have a value")
        with self.assertRaises(TypeError) as context:
            leaf_no_value = LeafNode("p")
            leaf_no_value.to_html()
            self.assertTrue("A leaf must have a value")
        
    def test_to_html(self):
        leaf_node = LeafNode("button", "Test", props={"class": "btn", "type": "button"})
        self.assertEqual(leaf_node.to_html(), '<button class="btn" type="button">Test</button>')

        leaf_node = LeafNode(None, "Test")
        self.assertEqual(leaf_node.to_html(), "Test")

    def test_repr(self):
        leaf_node = LeafNode("button", "Test", props={"class": "btn", "type": "button"})
        self.assertEqual(repr(leaf_node), '<button class="btn" type="button">Test</button>')

    def test_str(self):
        leaf_node = LeafNode("button", "Test", props={"class": "btn", "type": "button"})
        self.assertEqual(str(leaf_node), '<button class="btn" type="button">\n  Test\n</button>')