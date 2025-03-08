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

    
    
     