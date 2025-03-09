from processors.copy_tree import copy_tree
from processors.generate_page import generate_page
from constants import PUBLIC_PATH, STATIC_PATH

def main():
    # Clear ./public directory and copy everything from ./static to it.
    copy_tree(STATIC_PATH, PUBLIC_PATH)

    # Generate ./public/index.html using template.html and content/index.md.
    # The generated HTML will be wrapped in an <article> and inserted into the
    # template's body. 
    generate_page("./content/index.md", "./template.html", "./public/index.html", "article") 
main()
