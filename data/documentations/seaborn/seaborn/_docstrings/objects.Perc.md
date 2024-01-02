```python
import seaborn.objects as so
from seaborn import load_dataset
diamonds = load_dataset("diamonds")
```
The default behavior computes the quartiles and min/max of the input data:

```python
p = (
    so.Plot(diamonds, "cut", "price")
    .scale(y="log")
)
p.add(so.Dot(), so.Perc())
```
Passing an integer will compute that many evenly-spaced percentiles:

```python
p.add(so.Dot(), so.Perc(20))
```
Passing a list will compute exactly those percentiles:

```python
p.add(so.Dot(), so.Perc([10, 25, 50, 75, 90]))
```
Combine with a range mark to show a percentile interval:

```python
(
    so.Plot(diamonds, "price", "cut")
    .add(so.Dots(pointsize=1, alpha=.2), so.Jitter(.3))
    .add(so.Range(color="k"), so.Perc([25, 75]), so.Shift(y=.2))
    .scale(x="log")
)
```


```python

```
