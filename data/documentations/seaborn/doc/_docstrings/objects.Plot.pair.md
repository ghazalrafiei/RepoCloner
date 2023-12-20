.. currentmodule:: seaborn.objects

```python
import seaborn.objects as so
from seaborn import load_dataset
mpg = load_dataset("mpg")
```

Plot one dependent variable against multiple independent variables by assigning `y` and pairing on `x`:


```python
(
    so.Plot(mpg, y="acceleration")
    .pair(x=["displacement", "weight"])
    .add(so.Dots())
)
```

Show multiple pairwise relationships by passing lists to both `x` and `y`:


```python
(
    so.Plot(mpg)
    .pair(x=["displacement", "weight"], y=["horsepower", "acceleration"])
    .add(so.Dots())
)
```

When providing lists for both `x` and `y`, pass `cross=False` to pair each position in the list rather than showing all pairwise relationships:


```python
(
    so.Plot(mpg)
    .pair(
        x=["weight", "acceleration"],
        y=["displacement", "horsepower"],
        cross=False,
    )
    .add(so.Dots())
)
```

When plotting against several `x` or `y` variables, it is possible to `wrap` the subplots to produce a two-dimensional grid:


```python
(
    so.Plot(mpg, y="mpg")
    .pair(x=["displacement", "weight", "horsepower", "cylinders"], wrap=2)
    .add(so.Dots())
)
```

Pairing can be combined with faceting, either pairing on `y` and faceting on `col` or pairing on `x` and faceting on `row`:


```python
(
    so.Plot(mpg, x="weight")
    .pair(y=["horsepower", "acceleration"])
    .facet(col="origin")
    .add(so.Dots())
)
```

While typically convenient to assign pairing variables as references to the common `data`, it's also possible to pass a list of vectors:


```python
(
    so.Plot(mpg["weight"])
    .pair(y=[mpg["horsepower"], mpg["acceleration"]])
    .add(so.Dots())
)
```
When customizing the plot through methods like :meth:`Plot.label`, :meth:`Plot.limit`, or :meth:`Plot.scale`, you can refer to the individual coordinate variables as `x0`, `x1`, etc.:

```python
(
    so.Plot(mpg, y="mpg")
    .pair(x=["weight", "displacement"])
    .label(x0="Weight (lb)", x1="Displacement (cu in)", y="MPG")
    .add(so.Dots())
)
```


```python

```
