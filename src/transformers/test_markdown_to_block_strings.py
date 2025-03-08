from test_utils import TestRunner
from transformers.markdown_to_block_strings import markdown_to_block_strings

class TestMarkdownToBlockStrings(TestRunner):
    simple_cases = [
        {
            "name": "simple case",
            "text": "# This is a heading.\n\nThis is a paragraph of text.\n\nIt some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            "expected": [
                "# This is a heading.", 
                "This is a paragraph of text.", 
                "It some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ]
        },
        {
            "name": "strips extra whitespace",
            "text": "\n# This is a heading.\n\n\nThis is a paragraph of text.\n\nIt some **bold** and *italic* words inside of it. \n\n\n* This is the first list item in a list block\n * This leading or trailing space will not be stripped \n* This trailing space will be stripped \n\n## this trailing space will \n ",
            "expected": [
                "# This is a heading.", 
                "This is a paragraph of text.", 
                "It some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n * This leading or trailing space will not be stripped \n* This trailing space will be stripped",
                "## this trailing space will"
            ]
        },
        {
            "name": "code block",
            "text": "# code block example\n\n```python\nfor foo in bar:\n\tprint(foo)\n```\n\ntext",
            "expected": [
                "# code block example",
                "```python\nfor foo in bar:\n\tprint(foo)\n```",
                "text"
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
