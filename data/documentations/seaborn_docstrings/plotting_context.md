```python
import seaborn as sns
```

Calling with no arguments will return the current defaults for the parameters that get scaled:


```python
sns.plotting_context()
```

Calling with the name of a predefined style will show those values:


```python
sns.plotting_context("talk")
```

Use the function as a context manager to temporarily change the parameter values:


```python
with sns.plotting_context("talk"):
    sns.lineplot(x=["A", "B", "C"], y=[1, 3, 2])
```


```python

```
