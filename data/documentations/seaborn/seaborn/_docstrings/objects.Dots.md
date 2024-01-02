```python
import seaborn.objects as so
from seaborn import load_dataset
mpg = load_dataset("mpg")
```
This mark draws relatively small, partially-transparent dots:

```python
p1 = so.Plot(mpg, "horsepower", "mpg")
p1.add(so.Dots())
```
Fixing or mapping the `color` property changes both the stroke (edge) and fill:

```python
p1.add(so.Dots(), color="origin")
```
These properties can be independently parametrized (although the resulting plot may not always be clear):

```python
(
    p1.add(so.Dots(fillalpha=.5), color="origin", fillcolor="weight")
    .scale(fillcolor="binary")
)
```
Filled and unfilled markers will happily mix:

```python
p1.add(so.Dots(stroke=1), marker="origin").scale(marker=["o", "x", (6, 2, 1)])
```
The partial opacity also helps to see local density when using jitter:

```python
(
    so.Plot(mpg, "horsepower", "origin")
    .add(so.Dots(), so.Jitter(.25))
)
```


```python

```
