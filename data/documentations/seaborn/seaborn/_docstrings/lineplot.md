```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
sns.set_theme()
```
The ``flights`` dataset has 10 years of monthly airline passenger data:

```python
flights = sns.load_dataset("flights")
flights.head()
```
To draw a line plot using long-form data, assign the ``x`` and ``y`` variables:

```python
may_flights = flights.query("month == 'May'")
sns.lineplot(data=may_flights, x="year", y="passengers")
```
Pivot the dataframe to a wide-form representation:

```python
flights_wide = flights.pivot(index="year", columns="month", values="passengers")
flights_wide.head()
```
To plot a single vector, pass it to ``data``. If the vector is a :class:`pandas.Series`, it will be plotted against its index:

```python
sns.lineplot(data=flights_wide["May"])
```
Passing the entire wide-form dataset to ``data`` plots a separate line for each column:

```python
sns.lineplot(data=flights_wide)
```
Passing the entire dataset in long-form mode will aggregate over repeated values (each year) to show the mean and 95% confidence interval:

```python
sns.lineplot(data=flights, x="year", y="passengers")
```
Assign a grouping semantic (``hue``, ``size``, or ``style``) to plot separate lines

```python
sns.lineplot(data=flights, x="year", y="passengers", hue="month")
```
The same column can be assigned to multiple semantic variables, which can increase the accessibility of the plot:

```python
sns.lineplot(data=flights, x="year", y="passengers", hue="month", style="month")
```
Use the `orient` parameter to aggregate and sort along the vertical dimension of the plot:

```python
sns.lineplot(data=flights, x="passengers", y="year", orient="y")
```
Each semantic variable can also represent a different column. For that, we'll need a more complex dataset:

```python
fmri = sns.load_dataset("fmri")
fmri.head()
```
Repeated observations are aggregated even when semantic grouping is used:

```python
sns.lineplot(data=fmri, x="timepoint", y="signal", hue="event")
```
Assign both ``hue`` and ``style`` to represent two different grouping variables:

```python
sns.lineplot(data=fmri, x="timepoint", y="signal", hue="region", style="event")
```
When assigning a ``style`` variable, markers can be used instead of (or along with) dashes to distinguish the groups:

```python
sns.lineplot(
    data=fmri,
    x="timepoint", y="signal", hue="event", style="event",
    markers=True, dashes=False
)
```
Show error bars instead of error bands and extend them to two standard error widths:

```python
sns.lineplot(
    data=fmri, x="timepoint", y="signal", hue="event", err_style="bars", errorbar=("se", 2),
)
```
Assigning the ``units`` variable will plot multiple lines without applying a semantic mapping:

```python
sns.lineplot(
    data=fmri.query("region == 'frontal'"),
    x="timepoint", y="signal", hue="event", units="subject",
    estimator=None, lw=1,
)
```
Load another dataset with a numeric grouping variable:

```python
dots = sns.load_dataset("dots").query("align == 'dots'")
dots.head()
```
Assigning a numeric variable to ``hue`` maps it differently, using a different default palette and a quantitative color mapping:

```python
sns.lineplot(
    data=dots, x="time", y="firing_rate", hue="coherence", style="choice",
)
```
Control the color mapping by setting the ``palette`` and passing a :class:`matplotlib.colors.Normalize` object:

```python
sns.lineplot(
    data=dots.query("coherence > 0"),
    x="time", y="firing_rate", hue="coherence", style="choice",
     palette="flare", hue_norm=mpl.colors.LogNorm(),
)
```
Or pass specific colors, either as a Python list or dictionary:

```python
palette = sns.color_palette("mako_r", 6)
sns.lineplot(
    data=dots, x="time", y="firing_rate",
    hue="coherence", style="choice",
    palette=palette
)
```
Assign the ``size`` semantic to map the width of the lines with a numeric variable:

```python
sns.lineplot(
    data=dots, x="time", y="firing_rate",
    size="coherence", hue="choice",
    legend="full"
)
```
Pass a a tuple, ``sizes=(smallest, largest)``, to control the range of linewidths used to map the ``size`` semantic:

```python
sns.lineplot(
    data=dots, x="time", y="firing_rate",
    size="coherence", hue="choice",
    sizes=(.25, 2.5)
)
```
By default, the observations are sorted by ``x``. Disable this to plot a line with the order that observations appear in the dataset:

```python
x, y = np.random.normal(size=(2, 5000)).cumsum(axis=1)
sns.lineplot(x=x, y=y, sort=False, lw=1)
```
Use :func:`relplot` to combine :func:`lineplot` and :class:`FacetGrid`. This allows grouping within additional categorical variables. Using :func:`relplot` is safer than using :class:`FacetGrid` directly, as it ensures synchronization of the semantic mappings across facets:

```python
sns.relplot(
    data=fmri, x="timepoint", y="signal",
    col="region", hue="event", style="event",
    kind="line"
)
```
