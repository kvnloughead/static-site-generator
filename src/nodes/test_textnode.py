import unittest
from nodes.textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("Test", TextType.BOLD)
        node2 = TextNode("Test", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("Test", TextType.BOLD, "http://fake.png")
        node2 = TextNode("Test", TextType.BOLD, "http://fake.png")
        self.assertEqual(node, node2)

    def test_not_equal(self):
        node = TextNode("Test", TextType.BOLD, "http://fake.png")
        node2 = TextNode("Test", TextType.BOLD, "http://fake.PNG")
        node3 = TextNode("Test", TextType.BOLD)
        node4 = TextNode("Test", TextType.CODE, "http://fake.png")
        node5 = TextNode("XXX", TextType.BOLD, "http://fake.png")
        for other in [node2, node3, node4, node5]:
            self.assertNotEqual(node, other)

    def test_bad_type_exception(self):
        with self.assertRaises(AttributeError) as context:
            TextNode("Test", TextType.BAD_TYPE)
        self.assertTrue('type object "TextType" has no attribute "FAIL"')

    def test_repr(self):
        node = TextNode("Test", TextType.BOLD)
        node2 = TextNode("Test", TextType.BOLD, "http://fake.png")
        self.assertEqual(repr(node), "TextNode(Test, bold, None)")
        self.assertEqual(repr(node2), "TextNode(Test, bold, http://fake.png)")

if __name__ == "__main__":
    unittest.main()