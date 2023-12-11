"""
What does this files do?
1- clone github repos in config.py
2- saves metadata of that repo

TODO:
Add version
"""

import csv
import os
import shutil
import git
from config import GITHUB_REPOS_LINKS, STATS_FILE_DIR, DATA_DIR

if __name__ == '__main__':


    stats_file = open(STATS_FILE_DIR)
    csv_writer = csv.writer(stats_file)

    for repname, replink in GITHUB_REPOS_LINKS.items():
        if os.path.exists(os.path.join(DATA_DIR, repname)):
            shutil.rmtree(os.path.join(DATA_DIR, repname))
            print(f'{repname} directory was removed.')
        git.Repo.clone_from(replink, os.path.join(DATA_DIR, repname))
        print(f'{repname} is cloned.')
        # get_stats


