import os
from config import GITHUB_REPOS_LINKS, DATA_DIR

def ipynb_to_md_converter(ipynb_file):
    """
    ipynb_file: str
    """
    
def main():
    for repo in GITHUB_REPOS_LINKS.keys():
        repo_dir = os.path.join(DATA_DIR, repo)
        naive_document_extractor(repo_dir)

if __name__ == '__main__':
    main()