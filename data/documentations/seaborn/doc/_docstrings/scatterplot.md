```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme()
```
These examples will use the "tips" dataset, which has a mixture of numeric and categorical variables:

```python
tips = sns.load_dataset("tips")
tips.head()
```
Passing long-form data and assigning ``x`` and ``y`` will draw a scatter plot between two variables:

```python
sns.scatterplot(data=tips, x="total_bill", y="tip")
```
Assigning a variable to ``hue`` will map its levels to the color of the points:

```python
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="time")
```
Assigning the same variable to ``style`` will also vary the markers and create a more accessible plot:

```python
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="time", style="time")
```
Assigning ``hue`` and ``style`` to different variables will vary colors and markers independently:

```python
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="day", style="time")
```
If the variable assigned to ``hue`` is numeric, the semantic mapping will be quantitative and use a different default palette:

```python
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="size")
```
Pass the name of a categorical palette or explicit colors (as a Python list of dictionary) to force categorical mapping of the ``hue`` variable:

```python
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="size", palette="deep")
```
If there are a large number of unique numeric values, the legend will show a representative, evenly-spaced set:

```python
tip_rate = tips.eval("tip / total_bill").rename("tip_rate")
sns.scatterplot(data=tips, x="total_bill", y="tip", hue=tip_rate)
```
A numeric variable can also be assigned to ``size`` to apply a semantic mapping to the areas of the points:

```python
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="size", size="size")
```
Control the range of marker areas with ``sizes``, and set ``legend="full"`` to force every unique value to appear in the legend:

```python
sns.scatterplot(
    data=tips, x="total_bill", y="tip", hue="size", size="size",
    sizes=(20, 200), legend="full"
)
```
Pass a tuple of values or a :class:`matplotlib.colors.Normalize` object to ``hue_norm`` to control the quantitative hue mapping:

```python
sns.scatterplot(
    data=tips, x="total_bill", y="tip", hue="size", size="size",
    sizes=(20, 200), hue_norm=(0, 7), legend="full"
)
```
Control the specific markers used to map the ``style`` variable by passing a Python list or dictionary of marker codes:

```python
markers = {"Lunch": "s", "Dinner": "X"}
sns.scatterplot(data=tips, x="total_bill", y="tip", style="time", markers=markers)
```
Additional keyword arguments are passed to :meth:`matplotlib.axes.Axes.scatter`, allowing you to directly set the attributes of the plot that are not semantically mapped:

```python
sns.scatterplot(data=tips, x="total_bill", y="tip", s=100, color=".2", marker="+")
```
The previous examples used a long-form dataset. When working with wide-form data, each column will be plotted against its index using both ``hue`` and ``style`` mapping:

```python
index = pd.date_range("1 1 2000", periods=100, freq="m", name="date")
data = np.random.randn(100, 4).cumsum(axis=0)
wide_df = pd.DataFrame(data, index, ["a", "b", "c", "d"])
sns.scatterplot(data=wide_df)
```
Use :func:`relplot` to combine :func:`scatterplot` and :class:`FacetGrid`. This allows grouping within additional categorical variables, and plotting them across multiple subplots.

Using :func:`relplot` is safer than using :class:`FacetGrid` directly, as it ensures synchronization of the semantic mappings across facets.

```python
sns.relplot(
    data=tips, x="total_bill", y="tip",
    col="time", hue="day", style="day",
    kind="scatter"
)
```


```python

```
