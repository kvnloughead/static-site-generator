import os, re
from markdown_to_html_nodes.markdown_to_html_node import markdown_to_html_node
from processors.copy_tree import copy_tree
from constants import STATIC_PATH, PUBLIC_PATH

def extract_title(markdown):
    """
    Extracts the text of the top-level heading of the markdown (i.e., the block starting with a single #). Leading and trailing whitespace is stripped.
    
    If there is no h1, an exception is raised.
    """
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block.startswith("# "):
            return block.split(" ", maxsplit=1)[1].strip()
    raise ValueError("Expected markdown to contain one h1.")

def generate_page(from_path, template_path, dest_path, parent_tag="div"):
    """
    Takes a file of markdown (at from_path), converts it to HTML using markdown_to_html_node, extracts the title with extract_title, inserts the result into the template at template_path, and writes the completed HTML to a file at dest_path.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    
    with open(from_path, 'r') as file:
        markdown = file.read()

    with open(template_path, 'r') as file:
        template = file.read()

    title = extract_title(markdown)
    html = markdown_to_html_node(markdown, parent_tag)

    with_title = template.replace("{{ Title }}", title)
    with_content = with_title.replace("{{ Content }}", repr(html))

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(with_content)

def generate_pages_recursively(
        src_dirpath, template_path, dest_dirpath, tag="div"):

    source_tree = os.listdir(src_dirpath)
    if len(source_tree) == 0:
        raise OSError(f"Source path must not be empty.")

    for f in source_tree:
        src_path = os.path.join(src_dirpath, f)
        dest_file = re.sub(r'.md$', ".html", f)
        dest_path = os.path.join(dest_dirpath, dest_file)
        if os.path.isfile(src_path):
            generate_page(src_path, template_path, dest_path, tag)
        elif os.path.isdir(src_path):
            generate_pages_recursively(src_path, template_path, dest_path)
