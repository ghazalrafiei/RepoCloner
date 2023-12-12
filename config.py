import os

#TODO: Convert to variable
GITHUB_REPOS_LINKS = {
    'seaborn':'https://github.com/mwaskom/seaborn',
    'vscode':'https://github.com/microsoft/vscode',
    'cloc':'https://github.com/AlDanial/cloc',
    'nocodb':'https://github.com/nocodb/nocodb',
    'final-db-proj':'https://github.com/ghazalrafiei/Final-DB-Project',
    'tgdesktop':'https://github.com/telegramdesktop/tdesktop',
    'htop':'https://github.com/htop-dev/htop',
    'k8s':'https://github.com/kubernetes/kubernetes'
}
REPO_DOCUMENTS = {
    'seaborn':'doc/',
    'tgdesktop':'docs/',
    'cloc':'README.md',
    'final-db-proj':'README.md',
    'htop':['README.md','docs/'],
    #requires data scraping
    'vscode':'https://code.visualstudio.com/docs',
    'nocodb':'https://docs.nocodb.com/', 
}

#TODO: covern to variables
REPOS_STATS_COLUMNS = [
    'name',
    'tag', #version
    'SLOC',
    'release_date',
    'top_languages_in_order',
]

REPO_SIZE_LABELS={
    'small':(0,1000),
    'medium':(1000,10_000),
    'large':(10_000,100_000),
    'very large':(100_000, 1_000_000),
    'huge':(1_000_000,10_000_000)
}

DATA_DIR = './datasets/'
STATS_FILE_DIR =  os.path.join(DATA_DIR, 'stats.csv')
GH_TOKEN_DIR = './token.txt'