import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_bad_arguments(self):
        with self.assertRaises(TypeError) as context:
            null_node = HTMLNode()
        self.assertTrue("Must provide at least one of tag, value, or children")

    def test_props_to_html(self):
        button_node = HTMLNode(tag="button", value="Click me", 
                                children= None, props={ "class": "my-button", "type": "button"})
        self.assertEqual(button_node.props_to_html(), 
                            ' class="my-button" type="button"')
        
        no_props_node = HTMLNode(tag="button", value="Click me", 
                                children= None)
        self.assertEqual(no_props_node.props_to_html(), "")

    def test_get_opening_tag(self):
        img_node = HTMLNode(tag="img", children=None, props={ "src": "#"}, settings={ "isSelfClosing": True })
        self.assertEqual(img_node._get_opening_tag(), '<img src="#">')

        div_node = HTMLNode(tag="div", children=[img_node, img_node])
        self.assertEqual(div_node._get_opening_tag(), "<div>")

        text_node = HTMLNode(tag=None, value="Text")
        self.assertEqual(text_node._get_opening_tag(), "Text")

    def test_get_value(self):
        # Without indent
        button_node = HTMLNode(tag="button", value="Click me", children=None, props={ "class": "my-button", "type": "button"})
        self.assertEqual(button_node._get_value(), "Click me")

        # With indent
        button_node = HTMLNode(tag="button", value="Click me", children=None, props={ "class": "my-button", "type": "button"})
        self.assertEqual(button_node._get_value(2), "\n  Click me")

        # No value
        button_node = HTMLNode(tag="button", props={ "class": "my-button", "type": "button"})

    def test_get_closing_tag(self):
        div_node = HTMLNode(tag="div")
        self.assertEqual(div_node._get_closing_tag(), "</div>")

        raw_node = HTMLNode(tag="div", children=[div_node, div_node])
        self.assertEqual(raw_node._get_closing_tag(), "</div>")

        pretty_node = HTMLNode(tag="div", children=[div_node, div_node])
        self.assertEqual(pretty_node._get_closing_tag(0), "\n</div>")

        indented_node = HTMLNode(tag="div", children=[div_node, div_node])
        self.assertEqual(indented_node._get_closing_tag(2), "\n  </div>")

    def test_str_and_repr(self):
        p_node_1 = HTMLNode(tag="p", value="Paragraph 1", props={"class": "text"})
        p_node_2 = HTMLNode(tag="p", value="Paragraph 2")
        img_node = HTMLNode(tag="img", children=None, props={ "src": "#"}, settings={ "isSelfClosing": True })
        
        parent_node = HTMLNode(tag="div", children=[p_node_1, p_node_2])
        aunt_node = HTMLNode(tag="div", children=[img_node])

        granny_node = HTMLNode(tag="main", children=[parent_node, aunt_node])
        self.assertEqual(granny_node.__str__(0), '<main>\n  <div>\n    <p class="text">\n      Paragraph 1\n    </p>\n    <p>\n      Paragraph 2\n    </p>\n  </div>\n  <div>\n    <img src="#">\n  </div>\n</main>')

        self.assertEqual(repr(granny_node), '<main><div><p class="text">Paragraph 1</p><p>Paragraph 2</p></div><div><img src="#"></div></main>')        