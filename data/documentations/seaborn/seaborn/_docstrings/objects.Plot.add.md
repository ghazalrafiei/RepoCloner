```python
import seaborn.objects as so
from seaborn import load_dataset
tips = load_dataset("tips")
```
Every layer must be defined with a :class:`Mark`:

```python
p = so.Plot(tips, "total_bill", "tip").add(so.Dot())
p
```
Call :class:`Plot.add` multiple times to add multiple layers. In addition to the :class:`Mark`, layers can also be defined with :class:`Stat` or :class:`Move` transforms:

```python
p.add(so.Line(), so.PolyFit())
```
Multiple transforms can be stacked into a pipeline. 

```python
(
    so.Plot(tips, y="day", color="sex")
    .add(so.Bar(), so.Hist(), so.Dodge())
)
```
Layers have an "orientation", which affects the transforms and some marks. The orientation is typically inferred from the variable types assigned to `x` and `y`, but it can be specified when it would otherwise be ambiguous:

```python
(
    so.Plot(tips, x="total_bill", y="size", color="time")
    .add(so.Dot(alpha=.5), so.Dodge(), so.Jitter(.4), orient="y")
)
```
Variables can be assigned to a specific layer. Note the distinction between how `pointsize` is passed to :class:`Plot.add` — so it is *mapped* by a scale — while `color` and `linewidth` are passed directly to :class:`Line`, so they directly set the line's color and width:

```python
(
    so.Plot(tips, "total_bill", "tip")
    .add(so.Dots(), pointsize="size")
    .add(so.Line(color=".3", linewidth=3), so.PolyFit())
    .scale(pointsize=(2, 10))
)
```
Variables that would otherwise apply to the entire plot can also be *excluded* from a specific layer by setting their value to `None`:

```python
(
    so.Plot(tips, "total_bill", "tip", color="day")
    .facet(col="day")
    .add(so.Dot(color="#aabc"), col=None, color=None)
    .add(so.Dot())
)
```
Variables used only by the transforms *must* be passed at the layer level:

```python
(
    so.Plot(tips, "day")
    .add(so.Bar(), so.Hist(), weight="size")
    .label(y="Total patrons")
)
```
Each layer can be provided with its own data source. If a data source was provided in the constructor, the layer data will be joined using its index:

```python
(
    so.Plot(tips, "total_bill", "tip")
    .add(so.Dot(color="#aabc"))
    .add(so.Dot(), data=tips.query("size == 2"), color="time")
)
```
Providing a `label` will annotate the layer in the plot's legend:

```python
(
    so.Plot(tips, x="size")
    .add(so.Line(color="C1"), so.Agg(), y="total_bill", label="Bill")
    .add(so.Line(color="C2"), so.Agg(), y="tip", label="Tip")
    .label(y="Value")
)
```


```python

```
