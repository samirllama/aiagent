import unittest
from functions.get_files_info import get_files_info


BASE_DIR = "."

class TestGetFilesInfo(unittest.TestCase):
    def test_calculator_directory(self):
        result = get_files_info("calculator", BASE_DIR)

        self.assertIn('- tests.py', result)
        self.assertIn('- main.py', result)
        self.assertIn('- pkg', result)

        self.assertIn('file_size=', result)
        self.assertIn('is_dir=', result)

        print('Result for current directory:')
        print(result)

    def test_pkg_directory(self):
        result = get_files_info("calculator", "pkg")

        self.assertIn('- calculator.py', result)
        self.assertIn('- render.py', result)

        self.assertIn('file_size=', result)
        self.assertIn('is_dir=', result)

        print(f"Result for 'pkg' directory:")
        print(result)

    def test_bin_directory(self):
        result = get_files_info("calculator", "/bin")

        print(f"Result for '/bin' directory:")
        print(result)

    def test_path_traversal_attempt_is_denied(self):
        result = get_files_info("calculator", "../")

        print(f"Result for '../' directory:")
        print(result)


if __name__ == "__main__":
    unittest.main()
