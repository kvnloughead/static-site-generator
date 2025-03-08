import unittest

class TestRunner(unittest.TestCase):
    def assert_raises_exception(self, exception, expected, cb, *cb_args, **cb_kwargs):
        with self.assertRaises(exception) as context:
            cb(*cb_args, **cb_kwargs)
        self.assertTrue(expected in str(context.exception))

    def run_tests(self, cases, test_func):
        for case in cases:
            with self.subTest(case["name"]):
                test_func(case)