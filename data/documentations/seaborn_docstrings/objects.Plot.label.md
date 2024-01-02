```python
import seaborn.objects as so
from seaborn import load_dataset
penguins = load_dataset("penguins")
```
Use strings to override default labels:

```python
p = (
    so.Plot(penguins, x="bill_length_mm", y="bill_depth_mm")
    .add(so.Dot(), color="species")
)
p.label(x="Length", y="Depth", color="")
```
Pass a function to *modify* the default label:

```python
p.label(color=str.capitalize)
```

Use this method to set the title for a single-axes plot:


```python
p.label(title="Penguin species exhibit distinct bill shapes")
```

When faceting, the `title` parameter will modify default titles:


```python
p.facet("sex").label(title=str.upper)
```

And the `col`/`row` parameters will add labels to the title for each facet:


```python
p.facet("sex").label(col="Sex:")
```

If more customization is needed, a format string can work well:


```python
p.facet("sex").label(title="{} penguins".format)
```


```python
p
```
When adding labels for each layer, the `legend=` parameter sets the title for the legend:

```python
(
    so.Plot(penguins, x="species")
    .add(so.Line(color="C1"), so.Agg(), y="bill_length_mm", label="length")
    .add(so.Line(color="C2"), so.Agg(), y="bill_depth_mm", label="depth")
    .label(legend="Measurement")
)
```


```python

```
