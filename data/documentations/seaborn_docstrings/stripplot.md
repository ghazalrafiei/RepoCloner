```python
import seaborn as sns
sns.set_theme(style="whitegrid")
```
Assigning a single numeric variable shows its univariate distribution with points randomly "jittered" on the other axis:

```python
tips = sns.load_dataset("tips")
sns.stripplot(data=tips, x="total_bill")
```
Assigning a second variable splits the strips of points to compare categorical levels of that variable:

```python
sns.stripplot(data=tips, x="total_bill", y="day")
```
Show vertically-oriented strips by swapping the assignment of the categorical and numerical variables:

```python
sns.stripplot(data=tips, x="day", y="total_bill")
```
Prior to version 0.12, the levels of the categorical variable had different colors by default. To get the same effect, assign the `hue` variable explicitly:

```python
sns.stripplot(data=tips, x="total_bill", y="day", hue="day", legend=False)
```
Or you can assign a distinct variable to `hue` to show a multidimensional relationship:

```python
sns.stripplot(data=tips, x="total_bill", y="day", hue="sex")
```
If the `hue` variable is numeric, it will be mapped with a quantitative palette by default (note that this was not the case prior to version 0.12):

```python
sns.stripplot(data=tips, x="total_bill", y="day", hue="size")
```
Use `palette` to control the color mapping, including forcing a categorical mapping by passing the name of a qualitative palette:

```python
sns.stripplot(data=tips, x="total_bill", y="day", hue="size", palette="deep")
```
By default, the different levels of the `hue` variable are intermingled in each strip, but setting `dodge=True` will split them:

```python
sns.stripplot(data=tips, x="total_bill", y="day", hue="sex", dodge=True)
```
The random jitter can be disabled by setting `jitter=False`:

```python
sns.stripplot(data=tips, x="total_bill", y="day", hue="sex", dodge=True, jitter=False)
```

If plotting in wide-form mode, each numeric column of the dataframe will be mapped to both `x` and `hue`:


```python
sns.stripplot(data=tips)
```
To change the orientation while in wide-form mode, pass `orient` explicitly:

```python
sns.stripplot(data=tips, orient="h")
```
The `orient` parameter is also useful when both axis variables are numeric, as it will resolve ambiguity about which dimension to group (and jitter) along:

```python
sns.stripplot(data=tips, x="total_bill", y="size", orient="h")
```
By default, the categorical variable will be mapped to discrete indices with a fixed scale (0, 1, ...), even when it is numeric:

```python
sns.stripplot(
    data=tips.query("size in [2, 3, 5]"),
    x="total_bill", y="size", orient="h",
)
```
To disable this behavior and use the original scale of the variable, set `native_scale=True`:

```python
sns.stripplot(
    data=tips.query("size in [2, 3, 5]"),
    x="total_bill", y="size", orient="h",
    native_scale=True,
)
```
Further visual customization can be achieved by passing keyword arguments for :func:`matplotlib.axes.Axes.scatter`:

```python
sns.stripplot(
    data=tips, x="total_bill", y="day", hue="time",
    jitter=False, s=20, marker="D", linewidth=1, alpha=.1,
)
```
To make a plot with multiple facets, it is safer to use :func:`catplot` than to work with :class:`FacetGrid` directly, because :func:`catplot` will ensure that the categorical and hue variables are properly synchronized in each facet:

```python
sns.catplot(data=tips, x="time", y="total_bill", hue="sex", col="day", aspect=.5)
```


```python

```
