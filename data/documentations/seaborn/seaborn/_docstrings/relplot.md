These examples will illustrate only some of the functionality that :func:`relplot` is capable of. For more information, consult the examples for :func:`scatterplot` and :func:`lineplot`, which are used when ``kind="scatter"`` or ``kind="line"``, respectively.

```python
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="ticks")
```
To illustrate ``kind="scatter"`` (the default style of plot), we will use the "tips" dataset:

```python
tips = sns.load_dataset("tips")
tips.head()
```
Assigning ``x`` and ``y`` and any semantic mapping variables will draw a single plot:

```python
sns.relplot(data=tips, x="total_bill", y="tip", hue="day")
```
Assigning a ``col`` variable creates a faceted figure with multiple subplots arranged across the columns of the grid:

```python
sns.relplot(data=tips, x="total_bill", y="tip", hue="day", col="time")
```
Different variables can be assigned to facet on both the columns and rows:

```python
sns.relplot(data=tips, x="total_bill", y="tip", hue="day", col="time", row="sex")
```
When the variable assigned to ``col`` has many levels, it can be "wrapped" across multiple rows:

```python
sns.relplot(data=tips, x="total_bill", y="tip", hue="time", col="day", col_wrap=2)
```
Assigning multiple semantic variables can show multi-dimensional relationships, but be mindful to avoid making an overly-complicated plot.

```python
sns.relplot(
    data=tips, x="total_bill", y="tip", col="time",
    hue="time", size="size", style="sex",
    palette=["b", "r"], sizes=(10, 100)
)
```
When there is a natural continuity to one of the variables, it makes more sense to show lines instead of points. To draw the figure using :func:`lineplot`, set ``kind="line"``. We will illustrate this effect with the "fmri dataset:

```python
fmri = sns.load_dataset("fmri")
fmri.head()
```
Using ``kind="line"`` offers the same flexibility for semantic mappings as ``kind="scatter"``, but :func:`lineplot` transforms the data more before plotting. Observations are sorted by their ``x`` value, and repeated observations are aggregated. By default, the resulting plot shows the mean and 95% CI for each unit

```python
sns.relplot(
    data=fmri, x="timepoint", y="signal", col="region",
    hue="event", style="event", kind="line",
)
```
The size and shape of the figure is parametrized by the ``height`` and ``aspect`` ratio of each individual facet:

```python
sns.relplot(
    data=fmri,
    x="timepoint", y="signal",
    hue="event", style="event", col="region",
    height=4, aspect=.7, kind="line"
)
```
The object returned by :func:`relplot` is always a :class:`FacetGrid`, which has several methods that allow you to quickly tweak the title, labels, and other aspects of the plot:

```python
g = sns.relplot(
    data=fmri,
    x="timepoint", y="signal",
    hue="event", style="event", col="region",
    height=4, aspect=.7, kind="line"
)
(g.map(plt.axhline, y=0, color=".7", dashes=(2, 1), zorder=0)
  .set_axis_labels("Timepoint", "Percent signal change")
  .set_titles("Region: {col_name} cortex")
  .tight_layout(w_pad=0))
```
It is also possible to use wide-form data with :func:`relplot`:

```python
flights_wide = (
    sns.load_dataset("flights")
    .pivot(index="year", columns="month", values="passengers")
)
```
Faceting is not an option in this case, but the plot will still take advantage of the external legend offered by :class:`FacetGrid`:

```python
sns.relplot(data=flights_wide, kind="line")
```
