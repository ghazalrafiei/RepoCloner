```python
import seaborn.objects as so
from seaborn import load_dataset
healthexp = (
    load_dataset("healthexp")
    .pivot(index="Year", columns="Country", values="Spending_USD")
    .interpolate()
    .stack()
    .rename("Spending_USD")
    .reset_index()
    .sort_values("Country")
)
```


```python
p = so.Plot(healthexp, "Year", "Spending_USD").facet("Country", wrap=3)
p.add(so.Area())
```
The `color` property sets both the edge and fill color:

```python
p.add(so.Area(), color="Country")
```
It's also possible to map only the `edgecolor`:

```python
p.add(so.Area(color=".5", edgewidth=2), edgecolor="Country")
```
The mark is drawn as a polygon, but it can be combined with :class:`Line` to draw a shaded region by setting `edgewidth=0`:

```python
p.add(so.Area(edgewidth=0)).add(so.Line())
```
The layer's orientation defines the axis that the mark fills from:

```python
p.add(so.Area(), x="Spending_USD", y="Year", orient="y")
```
This mark can be stacked to show part-whole relationships:

```python
(
    so.Plot(healthexp, "Year", "Spending_USD", color="Country")
    .add(so.Area(alpha=.7), so.Stack())
)
```


```python

```
