```python
import seaborn as sns
import matplotlib.pyplot as plt
```

By default, seaborn plots will be made with the current values of the matplotlib rcParams:


```python
sns.barplot(x=["A", "B", "C"], y=[1, 3, 2])
```

Calling this function with no arguments will activate seaborn's "default" theme:


```python
sns.set_theme()
sns.barplot(x=["A", "B", "C"], y=[1, 3, 2])
```

Note that this will take effect for *all* matplotlib plots, including those not made using seaborn:


```python
plt.bar(["A", "B", "C"], [1, 3, 2])
```

The seaborn theme is decomposed into several distinct sets of parameters that you can control independently:


```python
sns.set_theme(style="whitegrid", palette="pastel")
sns.barplot(x=["A", "B", "C"], y=[1, 3, 2])
```

Pass `None` to preserve the current values for a given set of parameters:


```python
sns.set_theme(style="white", palette=None)
sns.barplot(x=["A", "B", "C"], y=[1, 3, 2])
```

You can also override any seaborn parameters or define additional parameters that are part of the matplotlib rc system but not included in the seaborn themes:


```python
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)
sns.barplot(x=["A", "B", "C"], y=[1, 3, 2])
```


```python

```
