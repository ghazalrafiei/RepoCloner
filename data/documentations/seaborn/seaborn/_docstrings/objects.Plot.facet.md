.. currentmodule:: seaborn.objects

```python
import seaborn.objects as so
from seaborn import load_dataset
penguins = load_dataset("penguins")
diamonds = load_dataset("diamonds")
```

Assigning a faceting variable will create multiple subplots and plot subsets of the data on each of them:


```python
p = so.Plot(penguins, "bill_length_mm", "bill_depth_mm").add(so.Dots())
p.facet("species")
```

Multiple faceting variables can be defined to create a two-dimensional grid:


```python
p.facet("species", "sex")
```

Facet variables can be provided as references to the global plot data or as vectors:


```python
p.facet(penguins["island"])
```

With a single faceting variable, arrange the facets or limit to a subset by passing a list of levels to `order`:


```python
p.facet("species", order=["Gentoo", "Adelie"])
```

With multiple variables, pass `order` as a dictionary:


```python
p.facet("species", "sex", order={"col": ["Gentoo", "Adelie"], "row": ["Female", "Male"]})
```

When the faceting variable has multiple levels, you can `wrap` it to distribute subplots across both dimensions:


```python
p = so.Plot(diamonds, x="carat", y="price").add(so.Dots())
p.facet("color", wrap=4)
```

Wrapping works only when there is a single variable, but you can wrap in either direction:


```python
p.facet(row="color", wrap=2)
```
Use :meth:`Plot.share` to specify whether facets should be scaled the same way:

```python
p.facet("clarity", wrap=3).share(x=False)
```
Use :meth:`Plot.label` to tweak the titles:

```python
p.facet("color").label(title="{} grade".format)
```


```python

```
