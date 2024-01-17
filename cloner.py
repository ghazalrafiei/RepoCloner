"""
What does this repo do?
1- clone github repos in config.py
2- saves metadata of that repo

TODO:
Add version --> in tags
What is code complexity? SCC
bad performance --> calculate ecc once using oop
"""

import pandas as pd
import os
import git
import io
from config import GITHUB_REPOS_LINKS, STATS_FILE_DIR, DATA_DIR, REPO_SIZE_LABELS
from config import NOT_CODE_FILE_FORMATS

import warnings
warnings.filterwarnings("ignore")


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


def get_top_selected_languages(repo_dir, k=3, output='langs'):
    langs = os.popen(f'scc {repo_dir} --sort code -f csv').read()
    df = pd.read_csv(io.StringIO(langs), sep=',')
    df.sort_values(by='Lines', inplace=True, ascending=False)
    top_langs = df[['Language', 'Code']]

    for f in NOT_CODE_FILE_FORMATS:
        if f in top_langs['Language'].tolist():
            top_langs.drop(
                top_langs[top_langs['Language'] == f].index, inplace=True)

    # print('098098')
    if output == 'langs':
        return top_langs['Language'].iloc[:k].tolist()

    elif output == 'df':
        return top_langs.iloc[:k]


def get_esloc(repo_dir):
    """Get the sum of effective source lines of code"""
    return get_top_selected_languages(repo_dir, output='df')['Code'].sum()


def get_tag(repo_dir):
    try:
        return git.Repo(repo_dir).tags[-1].name
    except:
        return ''


def get_size_label(repo_dir, esloc=None):
    """Based on ESLOC"""
    if esloc is None:
        esloc = get_esloc(repo_dir)
    for label, sloc_range in REPO_SIZE_LABELS.items():
        if esloc < sloc_range[1] and esloc > sloc_range[0]:
            return label
    return 'Huge'

def get_ctag_size(repo_dir):
    os.system(f'ctags -R --format=2 -n {repo_dir} > /dev/null 2>&1')
    line_counts = os.popen(f'wc -l tags').read()
    os.system(f'cat tags > {os.path.join(repo_dir, "tags")}')
    os.system('rm tags')
    print(line_counts)

    return line_counts.split()[0]

def main():
    stat_df = pd.DataFrame()

    for repo_name, replink in GITHUB_REPOS_LINKS.items():
        repo_dir = os.path.join(DATA_DIR, repo_name)
        if not os.path.exists(repo_dir):
            print(f'Cloning {repo_name} ...')
            git.Repo.clone_from(replink, repo_dir)

        stat = {}
        stat['name'] = repo_name
        stat['ESLOC'] = get_esloc(repo_dir)
        stat['SLOC'] = get_sloc(repo_dir)
        stat['size_label'] = get_size_label(repo_dir, stat['ESLOC'])
        stat['ctag_size'] = get_ctag_size(repo_dir)
        stat['index_factor'] = round(int(stat['ESLOC']) / int(stat['ctag_size']), 2)# what does it mean?
        stat['top_k_selected_languages'] = str(get_top_selected_languages(repo_dir))
        stat['top_k_languages'] = str(get_top_languages(repo_dir))
        stat['tag'] = get_tag(repo_dir)
        stat['link'] = replink

        stat_df = pd.concat(
            [stat_df, pd.DataFrame.from_records([stat])], ignore_index=True)
        
        print(f'{repo_name} done.')

    stat_df.sort_values(by='ESLOC', inplace=True)
    stat_df.to_csv(STATS_FILE_DIR, index=False)

    print(f'Stats saved to {STATS_FILE_DIR}')
    # print(stat_df)


def test():
    for repname, replink in GITHUB_REPOS_LINKS.items():
        repo_dir = os.path.join(DATA_DIR, repname)
        if not os.path.exists(repo_dir):
            print(f'Cloning {repname} ...')
            git.Repo.clone_from(replink, repo_dir)
        print(get_esloc(repo_dir))


if __name__ == '__main__':
    main()
    # test()
