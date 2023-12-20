import os
import glob
import shutil
from config import GITHUB_REPOS_LINKS, DATA_DIR, DOCS_DIR

def recursive_file_finder(dir, file_format):
    """
    dir: str
    file_format: str
    """

    return glob.glob(f'{dir}/**/*{file_format}', recursive=True)

def copy_files_with_same_structure(src_dir, dst_dir, file_format):
    """
    src_dir: str
    dst_dir: str
    file_format: str
    """
    files = recursive_file_finder(src_dir, file_format)
    for src in files:
        dest = src.replace(src_dir, dst_dir)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(src, dest)


def naive_document_extractor(repo_dir):
    """
    Methods:
    1. all readme files
    2. docs/
    3. docstrings
    """

    repo_name = repo_dir.split('/')[-1]
    doc_dir = os.path.join(DOCS_DIR, repo_name)
    if not os.path.exists(doc_dir):
        os.mkdir(doc_dir)
    
    copy_files_with_same_structure(repo_dir, doc_dir, '.md')
        

def main():
    for repo in GITHUB_REPOS_LINKS.keys():
        repo_dir = os.path.join(DATA_DIR, repo)
        naive_document_extractor(repo_dir)

if __name__ == '__main__':
    main()