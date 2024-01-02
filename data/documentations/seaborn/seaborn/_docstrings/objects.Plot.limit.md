```python
import seaborn.objects as so
```
By default, plot limits are automatically set to provide a small margin around the data (controlled by :meth:`Plot.theme` parameters `axes.xmargin` and `axes.ymargin`):

```python
p = so.Plot(x=[1, 2, 3], y=[1, 3, 2]).add(so.Line(marker="o"))
p
```
Pass a `min`/`max` tuple to pin the limits at specific values:

```python
p.limit(x=(0, 4), y=(-1, 6))
```

Reversing the `min`/`max` values will invert the axis:


```python
p.limit(y=(4, 0))
```
Use `None` for either side to maintain the default value:

```python
p.limit(y=(0, None))
```


```python

```
