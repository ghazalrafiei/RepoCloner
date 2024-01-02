```python
import seaborn.objects as so
from seaborn import load_dataset
fmri = load_dataset("fmri").query("region == 'parietal'")
seaice = (
    load_dataset("seaice")
    .assign(
        Day=lambda x: x["Date"].dt.day_of_year,
        Year=lambda x: x["Date"].dt.year,
    )
    .query("Year >= 1980")
    .astype({"Year": str})
    .pivot(index="Day", columns="Year", values="Extent")
    .filter(["1980", "2019"])
    .dropna()
    .reset_index()
)
```
The mark fills between pairs of data points to show an interval on the value axis:

```python
p = so.Plot(seaice, x="Day", ymin="1980", ymax="2019")
p.add(so.Band())
```
By default it draws a faint ribbon with no edges, but edges can be added:

```python
p.add(so.Band(alpha=.5, edgewidth=2))
```
The defaults are optimized for the main expected usecase, where the mark is combined with a line to show an errorbar interval:

```python
(
    so.Plot(fmri, x="timepoint", y="signal", color="event")
    .add(so.Band(), so.Est())
    .add(so.Line(), so.Agg())
)
```
When min/max values are not explicitly assigned or added in a transform, the band will cover the full extent of the data:

```python
(
    so.Plot(fmri, x="timepoint", y="signal", color="event")
    .add(so.Line(linewidth=.5), group="subject")
    .add(so.Band())
)
```


```python

```
