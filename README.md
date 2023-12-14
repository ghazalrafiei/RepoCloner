# Repo Cloner

A tool as a part of the project [Document Evaluator]() to clone GitHub repositories and save these metadata for each repo.

```
name
SLOC (source lines of code)
ESCLOC (effective lines of code)
tag (version)
top k used programming languages
top k effective programmin languages
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



```

Default: keeps the current version of the repo and downloads only when the repo doesn't exist.