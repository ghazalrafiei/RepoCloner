```python
import seaborn.objects as so
from seaborn import load_dataset
penguins = load_dataset("penguins")
```
A line segment is drawn for each datapoint, centered on the value along the orientation axis:

```python
p = so.Plot(penguins, "species", "body_mass_g", color="sex")
p.add(so.Dash())
```
A number of properties can be mapped or set directly:

```python
p.add(so.Dash(alpha=.5), linewidth="flipper_length_mm")
```
The mark has a `width` property, which is relative to the spacing between orientation values:

```python
p.add(so.Dash(width=.5))
```
When dodged, the width will automatically adapt:

```python
p.add(so.Dash(), so.Dodge())
```
This mark works well to show aggregate values when paired with a strip plot:

```python
(
    p
    .add(so.Dash(), so.Agg(), so.Dodge())
    .add(so.Dots(), so.Dodge(), so.Jitter())
)
```
When both coordinate variables are numeric, you can control the orientation explicitly:

```python
(
    so.Plot(
        penguins["body_mass_g"],
        penguins["flipper_length_mm"].round(-1),
    )
    .add(so.Dash(), orient="y")
)
```


```python

```
