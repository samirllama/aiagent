import unittest
from functions.get_file_content import get_file_content


class TestGetFilesContent(unittest.TestCase):
    def test_calculator_directory(self):
        result = get_file_content("calculator", "main.py")

        print('Result for current directory:')
        print(result)

    def test_pkg_directory(self):
        result = get_file_content("calculator", "pkg/calculator.py")

        print(f"Result for 'pkg/calculator.py':")
        print(result)

    def test_bin_directory(self):
        result = get_file_content("calculator", "/bin/cat")

        print(f"Result for '/bin/cat' directory:")
        print(result)

    def test_path_traversal_attempt_is_denied(self):
        result = get_file_content("calculator", "pkg/does_not_exist.py")

        print(f"Result for 'pkg/does_not_exist.py':")
        print(result)


if __name__ == "__main__":
    unittest.main()
