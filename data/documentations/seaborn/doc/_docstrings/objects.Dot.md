```python
import seaborn.objects as so
from seaborn import load_dataset
tips = load_dataset("tips")
glue = load_dataset("glue")
```
This mark draws relatively large, filled dots by default:

```python
p1 = so.Plot(tips, "total_bill", "tip")
p1.add(so.Dot())
```
While :class:`Dots` is a better choice for dense scatter plots, adding a thin edge can help to resolve individual points:

```python
p1.add(so.Dot(edgecolor="w"))
```

Dodging and jittering can also help to reduce overplotting, when appropriate:


```python
(
    so.Plot(tips, "total_bill", "day", color="sex")
    .add(so.Dot(), so.Dodge(), so.Jitter(.2))
)
```
The larger dot size makes this mark well suited to representing values along a nominal scale:

```python
p2 = so.Plot(glue, "Score", "Model").facet("Task", wrap=4).limit(x=(-5, 105))
p2.add(so.Dot())
```
A number of properties can be set or mapped:

```python
(
    p2
    .add(so.Dot(pointsize=6), color="Year", marker="Encoder")
    .scale(marker=["o", "s"], color="flare")
)
```
Note that the edge properties are parameterized differently for filled and unfilled markers; use `stroke` and `color` rather than `edgewidth` and `edgecolor` if the marker is unfilled:

```python
p2.add(so.Dot(stroke=1.5), fill="Encoder", color="Encoder")
```
Combine with :class:`Range` to show error bars:

```python
(
    so.Plot(tips, x="total_bill", y="day")
    .add(so.Dot(pointsize=3), so.Shift(y=.2), so.Jitter(.2))
    .add(so.Dot(), so.Agg())
    .add(so.Range(), so.Est(errorbar=("se", 2)))
)
```


```python

```
