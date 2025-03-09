from test_utils import TestRunner
from processors.generate_page import extract_title

class TestExtractTitleFromMarkdown(TestRunner):
    cases = [
        {
            "name": "one line",
            "markdown": "# Title",
            "expected_raise": False,
            "expected": "Title"
        },
        {
            "name": "title first",
            "markdown": "# Title\n\n more stuff",
            "expected_raise": False,
            "expected": "Title"
        },
        {
            "name": "title not first",
            "markdown": "stuff\n\n# Title",
            "expected_raise": False,
            "expected": "Title"
        },
        {
            "name": "whitespace stripped",
            "markdown": "#  stripped title  \n\nstuff",
            "expected_raise": False,
            "expected": "stripped title"
        },

        {
            "name": "only h2",
            "markdown": "## Not h1\n\nstuff",
            "expected_raise": True
        },
        {
            "name": "no heading",
            "markdown": "Not heading\n\nstuff",
            "expected_raise": True
        },
    ]

    def test_cases(self):
        def test_func(case):
            if not case["expected_raise"]:
                actual = extract_title(case["markdown"])
                self.assertEqual(actual, case["expected"])
            else:
                self.assert_raises_exception(
                    ValueError, 
                    "Expected markdown to contain one h1.", 
                    extract_title, 
                    case["markdown"]
                )
        self.run_tests(self.cases, test_func)