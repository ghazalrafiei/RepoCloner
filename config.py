import os

GITHUB_REPOS_LINKS = {
    'seaborn':'https://github.com/mwaskom/seaborn',
    'vscode':'https://github.com/microsoft/vscode',
    'cloc':'https://github.com/AlDanial/cloc',
    'nocodb':'https://github.com/nocodb/nocodb',
    'final-db-proj':'https://github.com/ghazalrafiei/Final-DB-Project'
}

#TODO: covern to variables
REPOS_STATS_COLUMNS = [
    'name',
    'tag', #version
    'SLOC',
    'release_date',
    'top_languages_in_order',
]

DATA_DIR = '../datasets/'
STATS_FILE_DIR =  os.path.join(DATA_DIR, 'stats.csv')
GH_TOKEN_DIR = './token.txt'