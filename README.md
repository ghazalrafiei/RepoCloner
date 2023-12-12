# Repo Cloner

A tool as a part of the project [Document Evaluator]() to clone GitHub repositories and save these metadata for each repo.

```
name
SLOC (source lines of code)
tag (version)
top k used programming languages
size label (defind in config.py)
link
```

## Config
Add your repository names and http links to them in the `config.py`.

## Run
```
python3 cloner.py
```

### Output
```
|name         |SLOC   |size_label|top_k_languages                     |tag          |link                                            |
|-------------|-------|----------|------------------------------------|-------------|------------------------------------------------|
|k8s          |5682873|huge      |['Go', 'JSON', 'YAML']              |v1.9.9-beta.0|https://github.com/kubernetes/kubernetes        |
|vscode       |1590687|huge      |['TypeScript', 'JSON', 'JavaScript']|vsda-v1.39.1 |https://github.com/microsoft/vscode             |
|htop         |33584  |large     |['C', 'C', 'Autoconf']              |3.2.2        |https://github.com/htop-dev/htop                |
|seaborn      |104154 |very large|['Python', 'SVG', 'Jupyter']        |v0.9.1.rc0   |https://github.com/mwaskom/seaborn              |
|cloc         |50248  |large     |['Perl', 'YAML', 'Markdown']        |v1.98        |https://github.com/AlDanial/cloc                |
|nocodb       |1688932|huge      |['SQL', 'TypeScript', 'JSON']       |v0.9.41      |https://github.com/nocodb/nocodb                |
|final-db-proj|905    |small     |['Python', 'SQL', 'gitignore']      |             |https://github.com/ghazalrafiei/Final-DB-Project|
|tgdesktop    |557948 |very large|['C++', 'C', 'Objective']           |v4.9.9       |https://github.com/telegramdesktop/tdesktop     |


```

Default: keeps the current version of the repo and downloads only when the repo doesn't exist.