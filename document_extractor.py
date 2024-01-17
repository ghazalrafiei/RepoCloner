import os
import shutil
import ast
import numpy
from config import GITHUB_REPOS_LINKS, DATA_DIR, DOCS_DIR, DOC_FILE_FORMATS, DOC_FOLDER_NAMES
from utils import recursive_file_finder
from comment_parser import comment_parser

numpy.sort_complex()
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
    1. all readme and .rst files
    2. docs/
    """

    repo_name = repo_dir.split('/')[-1]
    doc_dir = os.path.join(DOCS_DIR, repo_name)
    
    if not os.path.exists(doc_dir):
        os.mkdir(doc_dir)
    
    for file_format in DOC_FILE_FORMATS:
        copy_files_with_same_structure(repo_dir, doc_dir, file_format)
    
    for doc_folder_name in DOC_FOLDER_NAMES:
        src_dir = os.path.join(repo_dir, doc_folder_name)
        if os.path.exists(src_dir):
            dest_dir = os.path.join(doc_dir, repo_name)
            shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)

def raw_comment_extractor(repo_dir):

    files = recursive_file_finder(repo_dir,'.**')
    for src in files:
        src_format = src.split('.')[-1]
        if src_format in DOC_FILE_FORMATS:
            continue
        repo_name = repo_dir.split('/')[-1]
        doc_dir = os.path.join(DOCS_DIR, repo_name)
        dest = src.replace(repo_dir, doc_dir)
        comments = []
        try:
            comments = comment_parser.extract_comments(src)
        except Exception as e:
            print('ERROR: ', src.split('.')[-1], e, src, dest)
        
        if len(comments):
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            dest = dest.replace('.','_')+'.comment'
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, 'w') as f:
                for c in comments:
                    f.write(f"['text':'{c._text}','line_number':{c._line_number},'multiline':{c._multiline}]".strip()+'\n')

# def docstring_extractor(repo_dir):
#     # Python
#     files = recursive_file_finder( repo_dir, '.py')
#     print(len(files))
#     for src in files:
#         # dest = src.replace()
#         # os.makedirs(os.path.dirname(dest), exist_ok=True)
#         docstrings = extract_docstrings(open(src).read())
#         print(docstrings)
#         print('!')
    
#     # Java
#     # files = recursive_file_finder(os.path.join(DATA_DIR, repo_dir), '.java')


def main():
    for repo in GITHUB_REPOS_LINKS.keys():
        repo_dir = os.path.join(DATA_DIR, repo)
        naive_document_extractor(repo_dir)
        raw_comment_extractor(repo_dir)
        # docstring_extractor(repo_dir)


if __name__ == '__main__':
    main()
