See the :func:`regplot` docs for demonstrations of various options for specifying the regression model, which are also accepted here.

```python
import seaborn as sns
sns.set_theme(style="ticks")
penguins = sns.load_dataset("penguins")
```
Plot a regression fit over a scatter plot:

```python
sns.lmplot(data=penguins, x="bill_length_mm", y="bill_depth_mm")
```
Condition the regression fit on another variable and represent it using color:

```python
sns.lmplot(data=penguins, x="bill_length_mm", y="bill_depth_mm", hue="species")
```
Condition the regression fit on another variable and split across subplots:

```python
sns.lmplot(
    data=penguins, x="bill_length_mm", y="bill_depth_mm",
    hue="species", col="sex", height=4,
)
```
Condition across two variables using both columns and rows:

```python
sns.lmplot(
    data=penguins, x="bill_length_mm", y="bill_depth_mm",
    col="species", row="sex", height=3,
)
```
Allow axis limits to vary across subplots:

```python
sns.lmplot(
    data=penguins, x="bill_length_mm", y="bill_depth_mm",
    col="species", row="sex", height=3,
    facet_kws=dict(sharex=False, sharey=False),
)
```


```python

```
