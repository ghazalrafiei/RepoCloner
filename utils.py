import glob
import ast

def recursive_file_finder(dir, file_format):
    """
    dir: str
    file_format: str
    """

    return glob.glob(f'{dir}/**/*{file_format}', recursive=True)

def extract_docstrings(source_code):
    """
    Extract docstrings from a Python source code string.
    """
    tree = ast.parse(source_code)
    docstrings = {}

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
            docstring = ast.get_docstring(node)
            if docstring:
                # print(type(node))
                docstrings[node] = docstring

    return docstrings.values()
