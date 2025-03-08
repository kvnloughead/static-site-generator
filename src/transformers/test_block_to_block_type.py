from test_utils import TestRunner
from transformers.block_to_block_type import block_to_block_type, each_line_starts_with, is_ordered_list, BlockType

class TestBlockToBlockType(TestRunner):
    heading_cases = [
        ("h1", "# foo"),
        ("h2", "## foo"),
        ("h3", "### foo"),
        ("h4", "#### foo"),
        ("h5", "##### foo"),
        ("h6", "###### foo"),
    ]

    code_cases = [
        ("with language name", "```python\nprint('foobar')\n```"),
        ("no language name", "```\nprint('foobar')\n```"),
        ("multiple lines", "```python\nfor foo in bar:\n\tprint(foo)\n```"),
        ("no newlines", "```console.log('foobar')```"),
    ]

    quote_cases = [
        ("one line", "> you have nothing to fear but off by one errors"),
        ("multiple lines", "> cat on a tin roof\n> dogs in a pile\n> nothing left to do but smile"),
    ]

    ordered_list_cases = [
        ("simple case", "1. first line\n2. second line"),
        ("only one entry", "1. first line"),
    ]

    unordered_list_cases = [
        ("with asterisks", "* foo\n* bar"),
        ("with dashes", "- foo\n- bar"),
        ("one entry", "- foo"),
    ]

    paragraph_cases = [
        ("not a heading - no text", "#"),
        ("not a heading - 7 #s ", "####### foo"),
        ("not a heading - missing space", "#foo"),
        ("not a quote - missing >", "> foo\nbar\n> baz"),
        ("not a list - missing dots", "1 missing dot\n2 missing dot"),
        ("missing space after number", "1.first line\n2. second line"), 
        ("not a list - out of order", "1. foo\n3. bar"),
        ("not a list - mixed bullets", "* foo\n- bar"),
        ("not a list - missing space", "* foo\n*bar"),
    ]

    def test_cases(self):
        def run_test(cases, expected):
            for case_name, text,  in cases:
                with self.subTest(case_name):
                    actual = block_to_block_type(text)
                    self.assertEqual(actual, expected)
                    
        run_test(self.heading_cases, BlockType.HEADING)
        run_test(self.code_cases, BlockType.CODE)
        run_test(self.quote_cases, BlockType.QUOTE)
        run_test(self.ordered_list_cases, BlockType.ORDERED_LIST)
        run_test(self.unordered_list_cases, BlockType.UNORDERED_LIST)
        run_test(self.paragraph_cases, BlockType.PARAGRAPH)

class TestEachLineStartsWith(TestRunner):
    cases = [
        {
            "name": "multiple lines",
            "char": ">",
            "lines": ["> yes", "> yes", "> yes"],
            "expected": True
        },
        {
            "name": "split on newlines",
            "char": ">",
            "lines": "> cat on a tin roof\n> dogs in a pile\n> nothing left to do but smile".split("\n"),
            "expected": True
        },
        {
            "name": "one line",
            "char": ">",
            "lines": ["> you have nothing to fear but off by one errors"],
            "expected": True
        },                                                
    ]   

    def test_cases(self):
        for case in self.cases:
            with self.subTest(case["name"]):
                actual = each_line_starts_with(case["char"], case["lines"])
                self.assertEqual(actual, case["expected"])

class TestIsOrderedList(TestRunner):
    cases = [
        {
            "name": "multiple lines",
            "lines": ["1. yes", "2. yes", "3. yes"],
            "expected": True
        },
        {
            "name": "one line",
            "lines": ["1. yes"],
            "expected": True
        },
        {
            "name": "missing space",
            "lines": ["1.yes", "2. yes", "3. yes"],
            "expected": False
        },               
        {
            "name": "bad sequence",
            "lines": ["1. yes", "3. yes", "2. yes"],
            "expected": False
        },                                
        {
            "name": "gap in sequence",
            "lines": ["1. yes", "no", "2. yes"],
            "expected": False
        },
    ]   

    def test_cases(self):
        for case in self.cases:
            with self.subTest(case["name"]):
                actual = is_ordered_list(case["lines"])
                self.assertEqual(actual, case["expected"])