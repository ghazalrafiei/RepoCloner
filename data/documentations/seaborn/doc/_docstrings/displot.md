```python
import seaborn as sns; sns.set_theme(style="ticks")
```
The default plot kind is a histogram:

```python
penguins = sns.load_dataset("penguins")
sns.displot(data=penguins, x="flipper_length_mm")
```
Use the ``kind`` parameter to select a different representation:

```python
sns.displot(data=penguins, x="flipper_length_mm", kind="kde")
```

There are three main plot kinds; in addition to histograms and kernel density estimates (KDEs), you can also draw empirical cumulative distribution functions (ECDFs):


```python
sns.displot(data=penguins, x="flipper_length_mm", kind="ecdf")
```

While in histogram mode, it is also possible to add a KDE curve:


```python
sns.displot(data=penguins, x="flipper_length_mm", kde=True)
```

To draw a bivariate plot, assign both ``x`` and ``y``:


```python
sns.displot(data=penguins, x="flipper_length_mm", y="bill_length_mm")
```

Currently, bivariate plots are available only for histograms and KDEs:


```python
sns.displot(data=penguins, x="flipper_length_mm", y="bill_length_mm", kind="kde")
```

For each kind of plot, you can also show individual observations with a marginal "rug":


```python
g = sns.displot(data=penguins, x="flipper_length_mm", y="bill_length_mm", kind="kde", rug=True)
```
Each kind of plot can be drawn separately for subsets of data using ``hue`` mapping:

```python
sns.displot(data=penguins, x="flipper_length_mm", hue="species", kind="kde")
```

Additional keyword arguments are passed to the appropriate underlying plotting function, allowing for further customization:


```python
sns.displot(data=penguins, x="flipper_length_mm", hue="species", multiple="stack")
```
The figure is constructed using a :class:`FacetGrid`, meaning that you can also show subsets on distinct subplots, or "facets":

```python
sns.displot(data=penguins, x="flipper_length_mm", hue="species", col="sex", kind="kde")
```
Because the figure is drawn with a :class:`FacetGrid`, you control its size and shape with the ``height`` and ``aspect`` parameters:

```python
sns.displot(
    data=penguins, y="flipper_length_mm", hue="sex", col="species",
    kind="ecdf", height=4, aspect=.7,
)
```
The function returns the :class:`FacetGrid` object with the plot, and you can use the methods on this object to customize it further:

```python
g = sns.displot(
    data=penguins, y="flipper_length_mm", hue="sex", col="species",
    kind="kde", height=4, aspect=.7,
)
g.set_axis_labels("Density (a.u.)", "Flipper length (mm)")
g.set_titles("{col_name} penguins")
```
