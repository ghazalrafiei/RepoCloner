# Source Code Cloner and Analyser

## 1. Repo Gatherer

A tool as a part of the project [Document Evaluator]() to clone GitHub repositories and store these metadata for each repo in a csv file.

```
name
SLOC (source lines of code)
ESLOC (effective lines of code)
tag (version)
top k used programming languages
top k effective programming languages
size label (defind in config.py)
link
```

### Config
Add your repository names and http links to them in the `config.py`.

### Run

To clone repos and analyse summarize them
```
python cloner.py
```

#### Output
See [stats.csv](https://github.com/ghazalrafiei/RepoGatherer/blob/main/stats.csv).

### Description
Default: keeps the current version of the repo and downloads only when the repo doesn't exist.

## 2. Document Extractor

### Run
```
python document_extractor.py
```
#### Output
See [data/documentations/]().

#### Methods
```
naive_document_extractor()
raw_comment_extractor()
docstring_extractor
```

### Naive Documentation Extractor:

1. Extract all `.md` files, with the same structure in the doc directory.
2. Copy the folder named one of ['doc/', 'docs/' ... ]

## 3. Preprocessor

1. Convert `.ipynb` to `.md` using [nbconvert](https://github.com/jupyter/nbconvert).
