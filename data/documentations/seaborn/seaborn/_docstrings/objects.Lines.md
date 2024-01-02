```python
import seaborn.objects as so
from seaborn import load_dataset
seaice = load_dataset("seaice")
```
Like :class:`Line`, the mark draws a connecting line between sorted observations:

```python
so.Plot(seaice, "Date", "Extent").add(so.Lines())
```
Compared to :class:`Line`, this mark offers fewer settable properties, but it can have better performance when drawing a large number of lines:

```python
(
    so.Plot(
        x=seaice["Date"].dt.day_of_year,
        y=seaice["Extent"],
        color=seaice["Date"].dt.year
    )
    .facet(seaice["Date"].dt.year.round(-1))
    .add(so.Lines(linewidth=.5, color="#bbca"), col=None)
    .add(so.Lines(linewidth=1))
    .scale(color="ch:rot=-.2,light=.7")
    .layout(size=(8, 4))
    .label(title="{}s".format)
)
```


```python

```
