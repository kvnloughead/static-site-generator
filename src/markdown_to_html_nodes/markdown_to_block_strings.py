import re

def markdown_to_block_strings(markdown):
    """
    markdown_to_blocks accepts a string of markdown and splits it into block strings, where blocks are separated by an empty line (i.e., by two newline characters).

    Leading and trailing whitespace is stripped and multiple adjacent newlines are treated as one. 
    If the string is empty, a ValueError is raised.
    """
    if len(markdown) == 0:
        raise ValueError("The markdown string can't be empty")
    
    # Strip markdown of trailing and leading whitespace and deduplicate newlines
    stripped = markdown.strip('\n')
    stripped = re.sub(r'\n\n+', r'\n\n', stripped)

    # Split on newlines, strip each block, and return the list
    blocks = stripped.split('\n\n')
    stripped = map(lambda b: b.strip(), blocks)
    return list(stripped)
