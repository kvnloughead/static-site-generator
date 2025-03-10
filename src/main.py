import sys
from processors.copy_tree import copy_tree
from processors.generate_page import generate_pages_recursively
from constants import STATIC_PATH, TEMPLATE_PATH, CONTENT_PATH

def main():
    # URL_BASE_PATH is the base path where the content will be served.
    # "/" in development, "/repo-name/" on GitHub Pages.
    URL_BASE_PATH = sys.argv[1] or "/"

    # DEPLOY_FROM_PATH is the file path where the served content will be stored.
    # "/public" in development, "/docs" on GitHub Pages.
    DEPLOY_FROM_PATH = sys.argv[2] or "/public"

    # Clear ./public directory and copy everything from ./static to it.
    copy_tree(STATIC_PATH, DEPLOY_FROM_PATH, clear_dest_tree=True)

    # Generate HTML files from markdown files in the content directory and add
    # them to the public directory.
    generate_pages_recursively(CONTENT_PATH, TEMPLATE_PATH, DEPLOY_FROM_PATH, "article", base_path=URL_BASE_PATH)
main()
