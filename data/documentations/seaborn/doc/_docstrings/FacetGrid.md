```python
import seaborn as sns
sns.set_theme(style="ticks")
```

Calling the constructor requires a long-form data object. This initializes the grid, but doesn't plot anything on it:


```python
tips = sns.load_dataset("tips")
sns.FacetGrid(tips)
```
Assign column and/or row variables to add more subplots to the figure:

```python
sns.FacetGrid(tips, col="time", row="sex")
```
To draw a plot on every facet, pass a function and the name of one or more columns in the dataframe to :meth:`FacetGrid.map`:

```python
g = sns.FacetGrid(tips, col="time",  row="sex")
g.map(sns.scatterplot, "total_bill", "tip")
```
The variable specification in :meth:`FacetGrid.map` requires a positional argument mapping, but if the function has a ``data`` parameter and accepts named variable assignments, you can also use :meth:`FacetGrid.map_dataframe`:

```python
g = sns.FacetGrid(tips, col="time",  row="sex")
g.map_dataframe(sns.histplot, x="total_bill")
```
Notice how the bins have different widths in each facet. A separate plot is drawn on each facet, so if the plotting function derives any parameters from the data, they may not be shared across facets. You can pass additional keyword arguments to synchronize them. But when possible, using a figure-level function like :func:`displot` will take care of this bookkeeping for you:

```python
g = sns.FacetGrid(tips, col="time", row="sex")
g.map_dataframe(sns.histplot, x="total_bill", binwidth=2, binrange=(0, 60))
```
The :class:`FacetGrid` constructor accepts a ``hue`` parameter. Setting this will condition the data on another variable and make multiple plots in different colors. Where possible, label information is tracked so that a single legend can be drawn:

```python
g = sns.FacetGrid(tips, col="time", hue="sex")
g.map_dataframe(sns.scatterplot, x="total_bill", y="tip")
g.add_legend()
```
When ``hue`` is set on the :class:`FacetGrid`, however, a separate plot is drawn for each level of the variable. If the plotting function understands ``hue``, it is better to let it handle that logic. But it is important to ensure that each facet will use the same hue mapping. In the sample ``tips`` data, the ``sex`` column has a categorical datatype, which ensures this. Otherwise, you may want to use the `hue_order` or similar parameter:

```python
g = sns.FacetGrid(tips, col="time")
g.map_dataframe(sns.scatterplot, x="total_bill", y="tip", hue="sex")
g.add_legend()
```
The size and shape of the plot is specified at the level of each subplot using the ``height`` and ``aspect`` parameters:

```python
g = sns.FacetGrid(tips, col="day", height=3.5, aspect=.65)
g.map(sns.histplot, "total_bill")
```
If the variable assigned to ``col`` has many levels, it is possible to "wrap" it so that it spans multiple rows:

```python
g = sns.FacetGrid(tips, col="size", height=2.5, col_wrap=3)
g.map(sns.histplot, "total_bill")
```
To add horizontal or vertical reference lines on every facet, use :meth:`FacetGrid.refline`:

```python
g = sns.FacetGrid(tips, col="time", margin_titles=True)
g.map_dataframe(sns.scatterplot, x="total_bill", y="tip")
g.refline(y=tips["tip"].median())
```

You can pass custom functions to plot with, or to annotate each facet. Your custom function must use the matplotlib state-machine interface to plot on the "current" axes, and it should catch additional keyword arguments:


```python
import matplotlib.pyplot as plt
def annotate(data, **kws):
    n = len(data)
    ax = plt.gca()
    ax.text(.1, .6, f"N = {n}", transform=ax.transAxes)

g = sns.FacetGrid(tips, col="time")
g.map_dataframe(sns.scatterplot, x="total_bill", y="tip")
g.map_dataframe(annotate)
```
The :class:`FacetGrid` object has some other useful parameters and methods for tweaking the plot:

```python
g = sns.FacetGrid(tips, col="sex", row="time", margin_titles=True)
g.map_dataframe(sns.scatterplot, x="total_bill", y="tip")
g.set_axis_labels("Total bill ($)", "Tip ($)")
g.set_titles(col_template="{col_name} patrons", row_template="{row_name}")
g.set(xlim=(0, 60), ylim=(0, 12), xticks=[10, 30, 50], yticks=[2, 6, 10])
g.tight_layout()
g.savefig("facet_plot.png")
```


```python
import os
if os.path.exists("facet_plot.png"):
    os.remove("facet_plot.png")
```
You also have access to the underlying matplotlib objects for additional tweaking:

```python
g = sns.FacetGrid(tips, col="sex", row="time", margin_titles=True, despine=False)
g.map_dataframe(sns.scatterplot, x="total_bill", y="tip")
g.figure.subplots_adjust(wspace=0, hspace=0)
for (row_val, col_val), ax in g.axes_dict.items():
    if row_val == "Lunch" and col_val == "Female":
        ax.set_facecolor(".95")
    else:
        ax.set_facecolor((0, 0, 0, 0))
```


```python

```
