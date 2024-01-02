```python
import seaborn as sns
sns.set_theme(style="whitegrid")
```
Assigning a single numeric variable shows its univariate distribution with points adjusted along on the other axis such that they don't overlap:

```python
tips = sns.load_dataset("tips")
sns.swarmplot(data=tips, x="total_bill")
```
Assigning a second variable splits the groups of points to compare categorical levels of that variable:

```python
sns.swarmplot(data=tips, x="total_bill", y="day")
```
Show vertically-oriented swarms by swapping the assignment of the categorical and numerical variables:

```python
sns.swarmplot(data=tips, x="day", y="total_bill")
```
Prior to version 0.12, the levels of the categorical variable had different colors by default. To get the same effect, assign the `hue` variable explicitly:

```python
sns.swarmplot(data=tips, x="total_bill", y="day", hue="day", legend=False)
```
Or you can assign a distinct variable to `hue` to show a multidimensional relationship:

```python
sns.swarmplot(data=tips, x="total_bill", y="day", hue="sex")
```
If the `hue` variable is numeric, it will be mapped with a quantitative palette by default (note that this was not the case prior to version 0.12):

```python
sns.swarmplot(data=tips, x="total_bill", y="day", hue="size")
```
Use `palette` to control the color mapping, including forcing a categorical mapping by passing the name of a qualitative palette:

```python
sns.swarmplot(data=tips, x="total_bill", y="day", hue="size", palette="deep")
```
By default, the different levels of the `hue` variable are intermingled in each swarm, but setting `dodge=True` will split them:

```python
sns.swarmplot(data=tips, x="total_bill", y="day", hue="sex", dodge=True)
```
The "orientation" of the plot (defined as the direction along which quantitative relationships are preserved) is usually inferred automatically. But in ambiguous cases, such as when both axis variables are numeric, it can be specified:

```python
sns.swarmplot(data=tips, x="total_bill", y="size", orient="h")
```
When the local density of points is too high, they will be forced to overlap in the "gutters" of each swarm and a warning will be issued. Decreasing the size of the points can help to avoid this problem:

```python
sns.swarmplot(data=tips, x="total_bill", y="size", orient="h", size=3)
```
By default, the categorical variable will be mapped to discrete indices with a fixed scale (0, 1, ...), even when it is numeric:

```python
sns.swarmplot(
    data=tips.query("size in [2, 3, 5]"),
    x="total_bill", y="size", orient="h",
)
```
To disable this behavior and use the original scale of the variable, set `native_scale=True` (notice how this also changes the order of the variables on the y axis):

```python
sns.swarmplot(
    data=tips.query("size in [2, 3, 5]"),
    x="total_bill", y="size", orient="h",
    native_scale=True,
)
```
Further visual customization can be achieved by passing keyword arguments for :func:`matplotlib.axes.Axes.scatter`:

```python
sns.swarmplot(
    data=tips, x="total_bill", y="day",
    marker="x", linewidth=1, 
)
```
To make a plot with multiple facets, it is safer to use :func:`catplot` with `kind="swarm"` than to work with :class:`FacetGrid` directly, because :func:`catplot` will ensure that the categorical and hue variables are properly synchronized in each facet:

```python
sns.catplot(
    data=tips, kind="swarm",
    x="time", y="total_bill", hue="sex", col="day",
    aspect=.5
)
```


```python

```
