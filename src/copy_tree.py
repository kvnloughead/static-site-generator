import os, shutil

def copy_tree(src, dest, dest_must_exist=False, clear_dest_tree=False, dest_must_be_empty=False, create_all=False):
    """
    Recursively copy an entire directory tree rooted at src to a directory named dst and return the destination directory. This is my somewhat different partial implementation of shutil.copytree.

    Behavior can be configured with flags:

    - dest_must_exist: if True, the destination directory must already exist. (Default: False)
    - clear_dest_tree: if True, the destination's existing tree is cleared before copying

    OSErrors are raised if:

    - The source path doesn't exist
    - dest_exists_ok is false and the destination path exists
    - The destination path is not a directory
    - must_be_empty is true and the destination path is a non-empty directory

    Symlinks are not supported and will be ignored.
    """
    # If the source path isn't a directory, raise an OSError.
    if not os.path.exists(src) or not os.path.isdir(src):
        raise OSError(f"Source path must exist and be a directory (src = {src}).")

    # Base case: if source path is empty, return.
    source_tree = os.listdir(src)
    if len(source_tree) == 0:
        return

    # If the destination path doesn't exist, create an empty directory there.
    if not os.path.exists(dest):
        os.mkdir(dest)

    # Raise an exception if dest exists and is not a directory.
    if not os.path.isdir(dest):
        raise OSError(f"Destination path must be a directory. (dest = {dest})")
    
    dest_is_empty = len(os.listdir(dest)) != 0
    print(dest_is_empty)
    # Raise an exception if must_be_empty and dest is not empty.
    if dest_must_be_empty and dest_is_empty:
        raise OSError(f"Destination path must be an empty directory. (dest = {dest})")
    
    # If the destination is a directory and clear_dest_tree is true, clear the 
    # tree and recreate the destination directory.
    if dest_is_empty and clear_dest_tree:
        shutil.rmtree(dest)
        os.mkdir(dest)

    for f in source_tree:
        src_filepath = os.path.join(src, f)
        dest_filepath = os.path.join(dest, f)
        print(dest_filepath)
        if os.path.isfile(src_filepath):
            shutil.copy(src_filepath, dest)
        elif os.path.isdir(src_filepath):
            if not os.path.exists(dest_filepath):
                os.mkdir(dest_filepath)
            copy_tree(src_filepath, 
                      dest_filepath,
                      clear_dest_tree=False, 
                      must_be_empty=False, 
                      create_all=False)