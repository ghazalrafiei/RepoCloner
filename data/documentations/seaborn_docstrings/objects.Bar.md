```python
import seaborn.objects as so
from seaborn import load_dataset
penguins = load_dataset("penguins")
flights = load_dataset("flights").query("year == 1960")
```
The mark draws discrete bars from a baseline to provided values:

```python
so.Plot(flights["month"], flights["passengers"]).add(so.Bar())
```
The bars are oriented depending on the x/y variable types and the `orient` parameter:

```python
so.Plot(flights["passengers"], flights["month"]).add(so.Bar())
```

A common usecase will be drawing histograms on a variable with a nominal scale:


```python
so.Plot(penguins, x="species").add(so.Bar(), so.Hist())
```

When mapping additional variables, the bars will overlap by default:


```python
so.Plot(penguins, x="species", color="sex").add(so.Bar(), so.Hist())
```
Apply a move transform, such as a :class:`Dodge` or :class:`Stack` to resolve them:

```python
so.Plot(penguins, x="species", color="sex").add(so.Bar(), so.Hist(), so.Dodge())
```
A number of properties can be mapped or set:

```python
(
    so.Plot(
        penguins, x="species",
        color="sex", alpha="sex", edgestyle="sex",
    )
    .add(so.Bar(edgewidth=2), so.Hist(), so.Dodge("fill"))
)
```
Combine with :class:`Range` to plot an estimate with errorbars:

```python
(
    so.Plot(penguins, "body_mass_g", "species", color="sex")
    .add(so.Bar(alpha=.5), so.Agg(), so.Dodge())
    .add(so.Range(), so.Est(errorbar="sd"), so.Dodge())
)
```


```python

```
