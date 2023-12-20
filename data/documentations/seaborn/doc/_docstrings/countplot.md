```python
import seaborn as sns
sns.set_theme(style="whitegrid")
titanic = sns.load_dataset("titanic")
```
Show the count of value for a single categorical variable:

```python
sns.countplot(titanic, x="class")
```
Group by a second variable:

```python
sns.countplot(titanic, x="class", hue="survived")
```
Normalize the counts to show percentages:

```python
sns.countplot(titanic, x="class", hue="survived", stat="percent")
```
