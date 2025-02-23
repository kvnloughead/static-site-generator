import unittest

class TestRunner(unittest.TestCase):
    def assert_raises_exception(self, exception, expected, cb, *cb_args, **cb_kwargs):
        with self.assertRaises(exception) as context:
            cb(*cb_args, **cb_kwargs)
        self.assertTrue(expected in str(context.exception))