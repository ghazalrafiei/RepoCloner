import os
from config import GITHUB_REPOS_LINKS, DATA_DIR
from utils import recursive_file_finder

def ipynbs_to_md_converter(repo_dir):
    """
    ipynb_file: str
    """
    ipynb_files = recursive_file_finder(repo_dir, '.ipynb')
    for ipfile in ipynb_files:
        os.system(f'jupyter nbconvert --to markdown {ipfile}')

    
def main():
    for repo in GITHUB_REPOS_LINKS.keys():
        repo_dir = os.path.join(DATA_DIR, repo)
        ipynbs_to_md_converter(repo_dir)

if __name__ == '__main__':
    main()