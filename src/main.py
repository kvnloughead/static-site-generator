import sys
from processors.copy_tree import copy_tree
from processors.generate_page import generate_pages_recursively
from constants import PUBLIC_PATH, STATIC_PATH, DEPLOY_PATH, TEMPLATE_PATH, CONTENT_PATH

def main():
    BASE_PATH = sys.argv[1]
    # Clear ./public directory and copy everything from ./static to it.
    copy_tree(STATIC_PATH, PUBLIC_PATH, clear_dest_tree=True)

    # Generate HTML files from markdown files in the content directory and add
    # them to the public directory.
    generate_pages_recursively(CONTENT_PATH, TEMPLATE_PATH, PUBLIC_PATH, "article")
main()
