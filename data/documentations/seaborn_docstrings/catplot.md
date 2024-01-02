```python
import seaborn as sns
sns.set_theme(style="whitegrid")
```
By default, the visual representation will be a jittered strip plot:

```python
df = sns.load_dataset("titanic")
sns.catplot(data=df, x="age", y="class")
```

Use `kind` to select a different representation:


```python
sns.catplot(data=df, x="age", y="class", kind="box")
```

One advantage is that the legend will be automatically placed outside the plot:


```python
sns.catplot(data=df, x="age", y="class", hue="sex", kind="boxen")
```

Additional keyword arguments get passed through to the underlying seaborn function:


```python
sns.catplot(
    data=df, x="age", y="class", hue="sex",
    kind="violin", bw_adjust=.5, cut=0, split=True,
)
```

Assigning a variable to `col` or `row` will automatically create subplots. Control figure size with the `height` and `aspect` parameters:


```python
sns.catplot(
    data=df, x="class", y="survived", col="sex",
    kind="bar", height=4, aspect=.6,
)
```

For single-subplot figures, it is easy to layer different representations:


```python
sns.catplot(data=df, x="age", y="class", kind="violin", color=".9", inner=None)
sns.swarmplot(data=df, x="age", y="class", size=3)
```
Use methods on the returned :class:`FacetGrid` to tweak the presentation:

```python
g = sns.catplot(
    data=df, x="who", y="survived", col="class",
    kind="bar", height=4, aspect=.6,
)
g.set_axis_labels("", "Survival Rate")
g.set_xticklabels(["Men", "Women", "Children"])
g.set_titles("{col_name} {col_var}")
g.set(ylim=(0, 1))
g.despine(left=True)
```


```python

```
