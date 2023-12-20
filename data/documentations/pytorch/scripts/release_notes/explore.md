```python
import pandas as pd
import numpy as np
from pprint import pprint
from collections import Counter
import common
import math
```


```python
commit_list_df = pd.read_csv("results/classifier/commitlist.csv")
mean_authors=commit_list_df.query("category == 'Uncategorized' & topic != 'not user facing'").author.to_list()
counts = Counter(mean_authors)
commit_list_df.head()
```


```python
commit_list_df.category.describe()
```


```python
# The number un categorized and no topic commits
no_category = commit_list_df.query("category == 'Uncategorized' & topic != 'not user facing'")
print(len(no_category))
```


```python
# check for cherry-picked commits
example_sha = '55c76baf579cb6593f87d1a23e9a49afeb55f15a'
commit_hashes = set(commit_list_df.commit_hash.to_list())

example_sha[:11] in commit_hashes
```


```python
# Get the difference between known categories and categories from commits

diff_categories = set(commit_list_df.category.to_list()) - set(common.categories)
print(len(diff_categories))
pprint(diff_categories)
```


```python
# Counts of categories

```
