```python
import seaborn.objects as so
from seaborn import load_dataset
penguins = load_dataset("penguins")
```
By default, faceted plots will share all axes:

```python
p = (
    so.Plot(penguins, x="bill_length_mm", y="bill_depth_mm")
    .facet(col="species", row="sex")
    .add(so.Dots())
)
p
```
Set a coordinate variable to `False` to let each subplot adapt independently:

```python
p.share(x=False, y=False)
```

It's also possible to share only across rows or columns:


```python
p.share(x="col", y="row")
```
This method is also relevant for paired plots, which have different defaults. In this case, you would need to opt *in* to full sharing (although it may not always make sense):

```python
(
    so.Plot(penguins, y="flipper_length_mm")
    .pair(x=["bill_length_mm", "bill_depth_mm"])
    .add(so.Dots())
    .share(x=True)
)
```


```python

```
