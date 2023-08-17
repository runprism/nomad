"""
Example function for test case.
"""

# Imports
from pathlib import Path


# Functions
def write_txt_file():
    """
    Write a file to S3. This allows us to test whether our code actually works.
    """
    path = "s3://cloudrun/tests/"
    test_str = "Hello world from our `test_function` test case!"
    with open(Path(path) / "test_function.txt") as f:
        f.write(test_str)
