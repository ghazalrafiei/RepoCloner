import glob

def recursive_file_finder(dir, file_format):
    """
    dir: str
    file_format: str
    """

    return glob.glob(f'{dir}/**/*{file_format}', recursive=True)