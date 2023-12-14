"""
What does this files do?
1- clone github repos in config.py
2- saves metadata of that repo

TODO:
Add version --> in tags
What is code complexity? SCC
"""

import pandas as pd
import os
import git
from config import GITHUB_REPOS_LINKS, STATS_FILE_DIR, DATA_DIR, REPO_SIZE_LABELS

def get_version():
    pass

def get_sloc(repo_dir):
    output = os.popen(f'scc {repo_dir} -w').read()
    return int(output.splitlines()[-8].split()[5])

def get_top_languages(repo_dir, k=3):
    output = os.popen(f'scc {repo_dir} -w --sort code').read()
    try:
        top_langs = [line.split()[0] for line in output.splitlines()[3:3+k]]
    except:
        top_langs = [line.split()[0] for line in output.splitlines()[0]]

    return top_langs

def get_tag(repo_dir):
    try:
        return git.Repo(repo_dir).tags[-1].name
    except:
        return ''

def get_size_label(repo_dir, sloc=None):
    if sloc is None:
        sloc = get_sloc(repo_dir)
    
    for label, sloc_range in REPO_SIZE_LABELS.items():
        if sloc < sloc_range[1] and sloc > sloc_range[0]:
            return label
    return f'not defined - {sloc}'


if __name__ == '__main__':

    stat_df = pd.DataFrame()

    for repname, replink in GITHUB_REPOS_LINKS.items():
        repo_dir = os.path.join(DATA_DIR, repname)
        if not os.path.exists(repo_dir):
            print(f'Cloning {repname} ...')
            git.Repo.clone_from(replink, repo_dir)

        stat = {}
        stat['name'] = repname
        stat['SLOC'] = get_sloc(repo_dir)
        stat['size_label'] = get_size_label(repo_dir, stat['SLOC'])
        stat['top_k_languages'] = str(get_top_languages(repo_dir))
        stat['tag'] = get_tag(repo_dir)
        stat['link'] = replink

        stat_df = pd.concat([stat_df, pd.DataFrame.from_records([stat])], ignore_index=True)
    
    stat_df.sort_values(by='SLOC', inplace=True)
    stat_df.to_csv(STATS_FILE_DIR)
    print(f'Stats saved to {STATS_FILE_DIR}')
    print(stat_df)