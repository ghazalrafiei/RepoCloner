```python
import seaborn.objects as so
```

Control the overall dimensions of the figure with `size`:


```python
p = so.Plot().layout(size=(4, 4))
p
```
Subplots created by using :meth:`Plot.facet` or :meth:`Plot.pair` will shrink to fit in the available space:

```python
p.facet(["A", "B"], ["X", "Y"])
```

You may find that different automatic layout engines give better or worse results with specific plots:


```python
p.facet(["A", "B"], ["X", "Y"]).layout(engine="constrained")
```

With `extent`, you can control the size of the plot relative to the underlying figure. Because the notebook display adapts the figure background to the plot, this appears only to change the plot size in a notebook context. But it can be useful when saving or displaying through a `pyplot` GUI window:


```python
p.layout(extent=[0, 0, .8, 1]).show()
```


```python

```
