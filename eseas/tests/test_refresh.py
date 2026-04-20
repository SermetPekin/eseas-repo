from eseas import refresh, Path
from eseas.tests.test_utils import skip_if_unix
from eseas.core.refresh_excel import refresh , File ,check_and_get_files
import unittest
from pathlib import Path
import time  
import os 



@skip_if_unix
def test_refresh():
    ROOT = Path(r"./excel_files")

    if not ROOT.exists():
        return
    files = ["test.xlsx"]

    refresh(files, ROOT)


@skip_if_unix
def test_refresh2(capsys):
    
    with capsys.disabled():
            
        files = ["a.xlsx" , "b.xlsx" , "c.xlsx"]
        
        fs = check_and_get_files(files , root = None , dont_check = True  )
        assert all([isinstance(x.path, Path)  for x in fs ])
        
        fs = check_and_get_files(files , root = "SomeRoot" , dont_check = True  )
        for f in fs : 
            print(f.path)



@skip_if_unix
class TestFileClass(unittest.TestCase):

    def setUp(self):
        self.test_dir = Path("test_files")
        self.test_dir.mkdir(exist_ok=True)

        self.file1 = self.test_dir / "file1.xlsx"
        self.file1.touch()
        self.file2 = self.test_dir / "subdir" / "file2.xlsx"
        self.file2.parent.mkdir(exist_ok=True)
        self.file2.touch()
        self.non_existent_file = self.test_dir / "nonexistent.xlsx"

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)

    def test_file_creation_no_root(self):
        file_obj = File("test.txt", root=None)
        self.assertEqual(file_obj.path, Path("test.txt").absolute())

    def test_file_creation_with_root(self):
        file_obj = File("test.txt", root=self.test_dir)
        expected_path = (self.test_dir / "test.txt").absolute()
        self.assertEqual(file_obj.path, expected_path)

    def test_file_exists(self):
        file_obj = File(self.file1)
        self.assertTrue(file_obj.exists())

        file_obj = File(self.non_existent_file)
        self.assertFalse(file_obj.exists())

    def test_file_check_existing_file(self):
        file_obj = File(self.file1)
        file_obj.check()   

    def test_file_check_nonexistent_file(self):
        file_obj = File(self.non_existent_file)
        with self.assertRaises(ValueError):
            file_obj.check()

    def test_file_check_with_dont_check(self):
        file_obj = File(self.non_existent_file, dont_check=True)
        file_obj.check()  

    def test_file_refresh(self):
        file_obj = File(self.file1)
        file_obj.refresh()   


    def test_check_and_get_files_valid_files(self):
        files = ["file1.xlsx", "subdir/file2.xlsx"]
        file_list = list(check_and_get_files(files, root=self.test_dir))
        self.assertEqual(len(file_list), 2)
        expected_path_1 = (self.test_dir / "file1.xlsx").absolute()
        self.assertEqual(str(file_list[0]), f"<File [{expected_path_1}]>")

        expected_path_2 = (self.test_dir / "subdir" / "file2.xlsx").absolute()
        self.assertEqual(str(file_list[1]), f"<File [{expected_path_2}]>")


    def test_check_and_get_files_with_nonexistent_file(self):
        files = ["file1.xlsx", "nonexistent.xlsx"]
        with self.assertRaises(ValueError):
            list(check_and_get_files(files, root=self.test_dir))

    def test_check_and_get_files_with_dont_check(self):
        files = ["nonexistent.xlsx"]
        file_list = list(check_and_get_files(files, root=self.test_dir, dont_check=True))
        self.assertEqual(len(file_list), 1)
        
