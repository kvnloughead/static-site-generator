from test_utils import TestRunner
from transformers.markdown_to_block_strings import markdown_to_block_strings

class TestMarkdownToBlockString(TestRunner):
    simple_cases = [
        {
            "name": "simple case",
            "text": "# This is a heading.\nThis is a paragraph of text.\nIt some **bold** and *italic* words inside of it.\n* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            "expected": [
                "# This is a heading.", 
                "This is a paragraph of text.", 
                "It some **bold** and *italic* words inside of it.", "* This is the first list item in a list block", 
                "* This is a list item", 
                "* This is another list item"
            ]
        },
        {
            "name": "strips extra whitespace",
            "text": "   # This is a heading.    \n\n\nThis is a paragraph of text.\n   It some **bold** and *italic* words inside of it.\n* This is the first list item in a list block  \n\n* This is a list item  \n* This is another list item  \n\n",
            "expected": [
                "# This is a heading.", 
                "This is a paragraph of text.", 
                "It some **bold** and *italic* words inside of it.", "* This is the first list item in a list block", 
                "* This is a list item", 
                "* This is another list item"
            ]
        }
    ]

    def test_simple_cases(self):
        for case in self.simple_cases:
            with self.subTest(case["name"]):
                actual = markdown_to_block_strings(case["text"])
                self.assertEqual(actual, case["expected"])

    def test_empty_markdown(self):
        self.assert_raises_exception(ValueError, "The markdown string can't be empty", lambda: markdown_to_block_strings(""))