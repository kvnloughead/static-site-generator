from test_utils import TestRunner
from transformers.text_to_textnodes import text_to_textnodes
from nodes.textnode import TextNode, TextType

class TestTextToTextNodes(TestRunner):
     simple_cases = [
          {
               "name": "all types",
               "text": "Text **bold** and *italic* and `code` and ![an image](image.png) and [a link](https://foo.bar)",
               "expected": [
                    TextNode("Text ", TextType.NORMAL),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" and ", TextType.NORMAL),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" and ", TextType.NORMAL),
                    TextNode("code", TextType.CODE),
                    TextNode(" and ", TextType.NORMAL),
                    TextNode("an image", TextType.IMAGE, url="image.png"),
                    TextNode(" and ", TextType.NORMAL),
                    TextNode("a link", TextType.LINK, url="https://foo.bar"),
               ]
          },
          {
               "name": "adjacent",
               "text": "**bold text***italic text*`code`![an image](image.png)[a link](https://foo.bar)",
               "expected": [
                    TextNode("bold text", TextType.BOLD),
                    TextNode("italic text", TextType.ITALIC),
                    TextNode("code", TextType.CODE),
                    TextNode("an image", TextType.IMAGE, url="image.png"),
                    TextNode("a link", TextType.LINK, url="https://foo.bar"),
               ]
          },
          {
              "name": "image nested inside delimiter",
              "text": "*Here is a [link](https://foo.bar)*",
              "expected": [TextNode("Here is a ", TextType.NORMAL),
                           TextNode("link", TextType.LINK, url="https://foo.bar")]
          },
          {
              "name": "only normal text",
              "text": "Just some normal text",
              "expected": [TextNode("Just some normal text", TextType.NORMAL)]
          }
     ]

     def test_simple_cases(self):
          for case in self.simple_cases:
              with self.subTest(case["name"]):
                  actual = text_to_textnodes(case["text"])
                  self.assertEqual(actual, case["expected"])

     def test_empty_string(self):
          with self.assertRaises(Exception) as context:
              text_to_textnodes("")
          self.assertTrue('Text must not be empty')
    
