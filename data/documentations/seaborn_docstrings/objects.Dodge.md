```python
import seaborn.objects as so
from seaborn import load_dataset
tips = load_dataset("tips").astype({"time": str})
```
This transform modifies both the width and position (along the orientation axis) of marks that would otherwise overlap:

```python
(
    so.Plot(tips, "day", color="time")
    .add(so.Bar(), so.Count(), so.Dodge())
)
```
By default, empty space may appear when variables are not fully crossed:

```python
p = so.Plot(tips, "day", color="time")
p.add(so.Bar(), so.Count(), so.Dodge())
```
The `empty` parameter handles this case; use it to fill out the space:

```python
p.add(so.Bar(), so.Count(), so.Dodge(empty="fill"))
```
Or center the marks while using a consistent width:

```python
p.add(so.Bar(), so.Count(), so.Dodge(empty="drop"))
```
Use `gap` to add a bit of spacing between dodged marks:

```python
p = so.Plot(tips, "day", "total_bill", color="sex")
p.add(so.Bar(), so.Agg("sum"), so.Dodge(gap=.1))
```
When multiple semantic variables are used, each distinct group will be dodged:

```python
p.add(so.Dot(), so.Dodge(), fill="smoker")
```
Use `by` to dodge only a subset of variables:

```python
p.add(so.Dot(), so.Dodge(by=["color"]), fill="smoker")
```
When combining with other transforms (such as :class:`Jitter` or :class:`Stack`), be mindful of the order that they are applied in:

```python
p.add(so.Dot(), so.Dodge(), so.Jitter())
```


```python

```
