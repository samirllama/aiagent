import os
from typing import Optional

def count_file_chars(path: str, encoding= 'utf-8')-> Optional[int]:
    try:
        with open(path,'r', encoding=encoding) as f:
            content = f.read()
            return len(content)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    except FileNotFoundError:
        print(f"File path {path} not found")
        return None


def get_file_content(working_directory:str, file_path:str) -> str:
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_file_path,'r', encoding='utf-8') as f:
            content = f.read()
            if len(content) > 10000:
                truncated_content = content[:10000]
                message = f'[...File "{file_path}" truncated at 10000 characters]'
                return truncated_content + message
            else:
                return content
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'
    except FileNotFoundError:
        return f"File path {abs_file_path} not found"

