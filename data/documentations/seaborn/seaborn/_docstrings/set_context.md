```python
import seaborn as sns
```

Call the function with the name of a context to set the default for all plots:


```python
sns.set_context("notebook")
sns.lineplot(x=[0, 1, 2], y=[1, 3, 2])
```

You can independently scale the font elements relative to the current context:


```python
sns.set_context("notebook", font_scale=1.25)
sns.lineplot(x=[0, 1, 2], y=[1, 3, 2])
```

It is also possible to override some of the parameters with specific values:


```python
sns.set_context("notebook", rc={"lines.linewidth": 3})
sns.lineplot(x=[0, 1, 2], y=[1, 3, 2])
```


```python

```
