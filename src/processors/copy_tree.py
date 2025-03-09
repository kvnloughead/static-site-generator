import os, shutil, sys

def copy_tree(src, dest, dest_must_exist=False, clear_dest_tree=False, dest_must_be_empty=False, create_full_dest_path=True):
    """
    Recursively copy an entire directory tree rooted at src to a directory named dst and return the destination directory. This is my somewhat different partial implementation of shutil.copytree.

    Behavior can be configured with flags:

    - dest_must_exist: if True, the destination directory must already exist. (Default: False)
    - clear_dest_tree: if True, the destination's existing tree is cleared before copying (default: False)
    - dest_must_be_empty: if True, the destination directory must be empty if it exists (default: False)
    - create_full_dest_path: if True, missing parent directories in the destination path will be created (default: True)

    OSErrors are raised if:

    - The source path doesn't exist
    - dest_exists_ok is false and the destination path exists
    - The destination path is not a directory
    - must_be_empty is true and the destination path is a non-empty directory

    Symlinks are not supported and will be ignored.
    """
    def make_directory(dirpath, create_full_path):
        try:
            if create_full_path:
                os.makedirs(dirpath)
            else:
                os.mkdir(dirpath)
        except FileNotFoundError:
            raise OSError(f"Parent directory does not exist for path: {dirpath}")

    dest_exists = os.path.exists(dest)
    dest_is_directory = os.path.isdir(dest)
    src_exists = os.path.exists(src)
    src_is_directory = os.path.isdir(src)

    # If the source path isn't a directory, raise an OSError.
    if not src_exists or not src_is_directory:
        raise OSError(f"Source path must exist and be a directory.")

    # Base case: if source path is empty, return.
    source_tree = os.listdir(src)
    if len(source_tree) == 0:
        raise OSError(f"Source path must not be empty.")

    # If the destination path doesn't exist, create an empty directory there.
    if not dest_exists and dest_must_exist:
        raise OSError(f"Destination path must exist and be a directory.")
    elif not dest_exists:
        make_directory(dest, create_full_path=create_full_dest_path)

    # Raise an exception if dest exists and is not a directory.
    if dest_exists and not dest_is_directory:
        raise OSError(f"Destination path must be a directory.")
    
    # Raise an exception if must_be_empty and dest is not empty.
    dest_is_empty = dest_exists and len(os.listdir(dest)) != 0
    if dest_must_be_empty and dest_is_empty:
        raise OSError(f"Destination path must be an empty directory.")
    
    # If the destination is a directory and clear_dest_tree is true, clear the 
    # tree and recreate the destination directory.
    if dest_is_empty and clear_dest_tree:
        shutil.rmtree(dest)
        make_directory(dest, create_full_path=create_full_dest_path)

    for f in source_tree:
        src_filepath = os.path.join(src, f)
        dest_filepath = os.path.join(dest, f)
        if os.path.isfile(src_filepath):
            shutil.copy(src_filepath, dest)
        elif os.path.isdir(src_filepath):
            if not os.path.exists(dest_filepath):
                os.mkdir(dest_filepath)
            copy_tree(src_filepath, 
                      dest_filepath,
                      clear_dest_tree=False, 
                      dest_must_be_empty=False, 
                      create_full_dest_path=False)