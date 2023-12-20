```python
import seaborn.objects as so
from seaborn import load_dataset
penguins = load_dataset("penguins")
diamonds = load_dataset("diamonds")
```
Use this transform to layer multiple marks that would otherwise overlap and be hard to interpret:

```python
(
    so.Plot(penguins, "species", "body_mass_g")
    .add(so.Dots(), so.Jitter())
    .add(so.Range(), so.Perc([25, 75]), so.Shift(x=.2))
)
```
For y variables with a nominal scale, bear in mind that the axis will be inverted and a positive shift will move downwards:

```python
(
    so.Plot(diamonds, "carat", "clarity")
    .add(so.Dots(), so.Jitter())
    .add(so.Range(), so.Perc([25, 75]), so.Shift(y=.25))
)
```


```python

```
