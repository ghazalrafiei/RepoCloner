```python
import seaborn.objects as so
from seaborn import load_dataset
dowjones = load_dataset("dowjones")
fmri = load_dataset("fmri")
```

The mark draws a connecting line between sorted observations:


```python
so.Plot(dowjones, "Date", "Price").add(so.Line())
```

Change the orientation to connect observations along the opposite axis (`orient="y"` is redundant here; the plot would detect that the date variable has a lower orientation priority than the price variable):


```python
so.Plot(dowjones, x="Price", y="Date").add(so.Line(), orient="y")
```
To replicate the same line multiple times, assign a `group` variable (but consider using :class:`Lines` here instead):

```python
(
    fmri
    .query("region == 'parietal' and event == 'stim'")
    .pipe(so.Plot, "timepoint", "signal")
    .add(so.Line(color=".2", linewidth=1), group="subject")
)
```
When mapping variables to properties like `color` or `linestyle`, stat transforms are computed within each grouping:

```python
p = so.Plot(fmri, "timepoint", "signal", color="region", linestyle="event")
p.add(so.Line(), so.Agg())
```
Combine with :class:`Band` to show an error bar:

```python
(
    p
    .add(so.Line(), so.Agg())
    .add(so.Band(), so.Est(), group="event")
)
```
Add markers to indicate values where the data were sampled:

```python
p.add(so.Line(marker="o", edgecolor="w"), so.Agg(), linestyle=None)
```


```python

```
