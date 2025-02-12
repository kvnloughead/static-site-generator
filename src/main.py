from textnode import TextNode, TextType

def main():
    text_node = TextNode("Text", TextType.BOLD, "http://fake.png")
    print(text_node)

main()
