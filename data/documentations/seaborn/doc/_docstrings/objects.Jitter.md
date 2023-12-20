```python
import seaborn.objects as so
from seaborn import load_dataset
penguins = load_dataset("penguins")
```
When used without any arguments, a small amount of jitter will be applied along the orientation axis:

```python
(
    so.Plot(penguins, "species", "body_mass_g")
    .add(so.Dots(), so.Jitter())
)
```
The `width` parameter controls the amount of jitter relative to the spacing between the marks:

```python
(
    so.Plot(penguins, "species", "body_mass_g")
    .add(so.Dots(), so.Jitter(.5))
)
```
The `width` parameter always applies to the orientation axis, so the direction of jitter will adapt along with the orientation:

```python
(
    so.Plot(penguins, "body_mass_g", "species")
    .add(so.Dots(), so.Jitter(.5))
)
```
Because the `width` jitter is relative, it can be used when the orientation axis is numeric without further tweaking:

```python
(
    so.Plot(penguins["body_mass_g"].round(-3), penguins["flipper_length_mm"])
    .add(so.Dots(), so.Jitter())
)
```
In contrast to `width`, the `x` and `y` parameters always refer to specific axes and control the jitter in data units:

```python
(
    so.Plot(penguins["body_mass_g"].round(-3), penguins["flipper_length_mm"])
    .add(so.Dots(), so.Jitter(x=100))
)
```
Both `x` and `y` can be used in a single transform:

```python
(
    so.Plot(
        penguins["body_mass_g"].round(-3),
        penguins["flipper_length_mm"].round(-1),
    )
    .add(so.Dots(), so.Jitter(x=200, y=5))
)
```


```python

```
