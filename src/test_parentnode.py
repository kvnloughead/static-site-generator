import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_without_children(self):
        with self.assertRaises(ValueError) as context:
            parent = ParentNode("div", None)
            parent.to_html()
        self.assertTrue("A parent node must have children")

        with self.assertRaises(ValueError) as context:
            parent = ParentNode("div", [])
            parent.to_html()
        self.assertTrue("A parent node must have children")

    def test_without_tag(self):
        with self.assertRaises(ValueError) as context:
            child = ParentNode("div", None)
            parent = ParentNode(None, [child])
            parent.to_html()
        self.assertTrue("A parent node must have children")

        with self.assertRaises(ValueError) as context:
            child = ParentNode("div", None)
            parent = ParentNode("", [child])
            parent.to_html()
        self.assertTrue("A parent node must have children")

    def test_to_html(self):
        leaf_1 = LeafNode("p", "Leaf 1")
        leaf_2 = LeafNode("p", "Leaf 2")
        parent_2 = ParentNode("div", [leaf_1, leaf_2], props={"class" : "parent", "id": "this-parent"})
        parent_1 = ParentNode("section", [leaf_1, parent_2], props={"class" : "parent", "id": "this-parent"})
        grandparent = ParentNode("section", [leaf_1, leaf_2, parent_1], props={"class" : "parent", "id": "this-parent"})
        self.assertEqual(grandparent.to_html(), '<section class="parent" id="this-parent"><p>Leaf 1</p><p>Leaf 2</p><section class="parent" id="this-parent"><p>Leaf 1</p><div class="parent" id="this-parent"><p>Leaf 1</p><p>Leaf 2</p></div></section></section>')

    def test_str(self):
        leaf = LeafNode("button", "Test", props={"class": "btn", "type": "button"})

        parent = ParentNode(tag="button", children=[leaf, leaf], props={"class": "btn", "type": "button"})

        self.assertEqual(str(parent), '<button class="btn" type="button">\n  <button class="btn" type="button">\n    Test\n  </button>\n  <button class="btn" type="button">\n    Test\n  </button>\n</button>')        
    