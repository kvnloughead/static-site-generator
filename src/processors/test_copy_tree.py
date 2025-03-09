import os, shutil
from test_utils import TestRunner
from processors.copy_tree import copy_tree

class TestCopyTree(TestRunner):
    def setUp(self):
        super().setUp()
        self.test_dir = '/tmp/test_copy_tree'
        self.src_dir = os.path.join(self.test_dir, 'src')
        self.dest_dir = os.path.join(self.test_dir, 'dest')

    def tearDown(self):
        try: 
            shutil.rmtree(self.test_dir)
        except FileNotFoundError:
            pass
        return super().tearDown()
    
    def _setup_empty_src(self):
        os.makedirs(self.test_dir, exist_ok=True)
        os.makedirs(self.src_dir, exist_ok=True)
    
    def _setup_full_src(self):
        self._setup_empty_src()
        with open(os.path.join(self.src_dir, 'file1.txt'), 'w') as f:
            f.write('This is file 1')
        
        with open(os.path.join(self.src_dir, 'file2.txt'), 'w') as f:
            f.write('This is file 2')
        
        os.makedirs(os.path.join(self.src_dir, 'subdir'), exist_ok=True)
        with open(os.path.join(self.src_dir, 'subdir', 'file3.txt'), 'w') as f:
            f.write('This is file 3')
    
    def _setup_full_dest(self):
        os.makedirs(self.dest_dir, exist_ok=True)
        with open(os.path.join(self.dest_dir, 'dest-file.txt'), 'w') as f:
            f.write('This file is unique to dest')
        with open(os.path.join(self.dest_dir, 'file1.txt'), 'w') as f:
            f.write('This file matches a src filename but with different content')
    
    def setup_src_and_dest(self):
        self._setup_full_src()
        self._setup_full_dest()        
    
    def _test_success(self, dest_dir=None):
        if not dest_dir:
            dest_dir = self.dest_dir
         # Check if files are copied correctly
        assert os.path.exists(os.path.join(dest_dir, 'file1.txt'))
        assert os.path.exists(os.path.join(dest_dir, 'file2.txt'))
        assert os.path.exists(os.path.join(dest_dir, 'subdir', 'file3.txt'))
        
        # Check the content of the copied files
        with open(os.path.join(dest_dir, 'file1.txt'), 'r') as f:
            assert f.read() == 'This is file 1'
        
        with open(os.path.join(dest_dir, 'file2.txt'), 'r') as f:
            assert f.read() == 'This is file 2'
        
        with open(os.path.join(dest_dir, 'subdir', 'file3.txt'), 'r') as f:
            assert f.read() == 'This is file 3'

        # Pre-existing file not removed by default.
        with open(os.path.join(dest_dir, 'dest-file.txt'), 'r') as f:
            assert f.read() == 'This file is unique to dest'

    def test_with_success_with_defaults(self):
        self.setup_src_and_dest()
        copy_tree(self.src_dir, self.dest_dir)
        self._test_success()    
    
    def test_empty_src(self):
        self._setup_empty_src()
        with self.assertRaises(OSError) as context:
            copy_tree(self.src_dir, "/tmp/non-existent")
        self.assertTrue("Source path must not be empty." in str(context.exception))

    def test_dest_must_exist_success(self):
        self.setup_src_and_dest()
        copy_tree(self.src_dir, self.dest_dir, dest_must_exist=True)
        self._test_success()

    def test_dest_must_exist_failure(self):
        self._setup_full_src()
        with self.assertRaises(OSError) as context:
            copy_tree(self.src_dir, "/tmp/non-existent", dest_must_exist=True)
        self.assertTrue("Destination path must exist and be a directory." in str(context.exception))

    def test_clear_dest_tree(self):
        self.setup_src_and_dest()
        copy_tree(self.src_dir, self.dest_dir, clear_dest_tree=True)
        self.assertFalse(os.path.exists(self.dest_dir + "/dest-file.txt"))
        
    def test_dest_must_empty(self):
        self.setup_src_and_dest()
        with self.assertRaises(OSError) as context:
            copy_tree(self.src_dir, self.dest_dir, dest_must_be_empty=True)
        self.assertTrue("Destination path must be an empty directory." in str(context.exception))
        
    def test_create_full_path_success(self):
        deep_dest = os.path.join("foo", "bar", self.dest_dir)
        self.setup_src_and_dest()
        copy_tree(self.src_dir, deep_dest, create_full_dest_path=True)
        self._test_success(dest_dir=deep_dest)

    def test_create_full_path_false(self):
        self._setup_full_src()
        with self.assertRaises(OSError) as context:
            copy_tree(self.src_dir, "/tmp/foo/bar/baz", create_full_dest_path=False)
        self.assertTrue("Parent directory does not exist for path: /tmp/foo/bar/baz" in str(context.exception))