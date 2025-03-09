from test_utils import TestRunner
from nodes.voidnode import VoidNode

class TestVoidNode(TestRunner):
    cases = [
        {
            "name": "image",
            "node_params": {
                "tag": "img",
                "props": {
                    "src": "img.png",
                    "alt": "alt text"
                }
            },
            "expected_repr": '<img src="img.png" alt="alt text">',
            "expected_exception": False
         },
         {
             "name": "br",
             "node_params": {
                "tag": "br",
            },
            "expected_repr": '<br>',
            "expected_exception": False
         },

         {
            "name": "image",
            "node_params": {
                "tag": None,
                "props": {
                    "src": "img.png",
                    "alt": "alt text"
                }
            },
            "expected_repr": "",
            "expected_exception": (TypeError, "A VoidNode must have a tag.")
         }
    ]

    def test_cases(self):
        def run_test(case):
            if case["expected_exception"]:
                exception, msg = case["expected_exception"]
                self.assert_raises_exception(
                    exception, 
                    msg, 
                    lambda: VoidNode(**case["node_params"]))
            else:
                node = VoidNode(**case["node_params"])
                self.assertEqual(repr(node), case["expected_repr"])
        self.run_tests(self.cases, run_test)