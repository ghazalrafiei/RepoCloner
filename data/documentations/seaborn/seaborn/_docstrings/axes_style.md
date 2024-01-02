```python
import seaborn as sns
```

Calling with no arguments will return the current defaults for the style parameters:


```python
sns.axes_style()
```

Calling with the name of a predefined style will show those parameter values:


```python
sns.axes_style("darkgrid")
```

Use the function as a context manager to temporarily change the style of your plots:


```python
with sns.axes_style("whitegrid"):
    sns.barplot(x=[1, 2, 3], y=[2, 5, 3])
```
