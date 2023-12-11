import os

GITHUB_REPOS_LINKS = {
    'seaborn':'https://github.com/mwaskom/seaborn',
    'vscode':'https://github.com/microsoft/vscode',
    'cloc':'https://github.com/AlDanial/cloc',
}

REPOS_STATS_COLUMNS = [
    'name',
    'version',
    'lines_of_code',
    'date',
    'languages_in_order',
]

DATA_DIR = '../datasets/'
STATS_FILE_DIR =  os.path.join(DATA_DIR, 'stats.csv')
GH_TOKEN_DIR = './token.txt'