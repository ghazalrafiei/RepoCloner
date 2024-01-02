.. currentmodule:: seaborn.objects

```python
%config InlineBackend.figure_format = "retina"
import seaborn as sns
import seaborn.objects as so
import matplotlib as mpl
import matplotlib.pyplot as plt
from seaborn import load_dataset
diamonds = load_dataset("diamonds")
```
Passing a :class:`matplotlib.axes.Axes` object provides functionality closest to seaborn's axes-level plotting functions. Notice how the resulting image looks different from others created with :class:`Plot`. This is because the plot theme uses the global rcParams at the time the axes were created, rather than :class:`Plot` defaults:

```python
p = so.Plot(diamonds, "carat", "price").add(so.Dots())
f, ax = plt.subplots()
p.on(ax).show()
```
Alternatively, calling :func:`matplotlib.pyplot.figure` will defer axes creation to :class:`Plot`, which will apply the default theme (and any customizations specified with :meth:`Plot.theme`):

```python
f = plt.figure()
p.on(f).show()
```
Creating a :class:`matplotlib.figure.Figure` object will bypass `pyplot` altogether. This may be useful for embedding :class:`Plot` figures in a GUI application:

```python
f = mpl.figure.Figure()
p.on(f).plot()
```
Using :class:`Plot.on` also provides access to the underlying matplotlib objects, which may be useful for deep customization. But it requires a careful attention to the order of operations by which the :class:`Plot` is specified, compiled, customized, and displayed:

```python
f = mpl.figure.Figure()
res = p.on(f).plot()

ax = f.axes[0]
rect = mpl.patches.Rectangle(
    xy=(0, 1), width=.4, height=.1,
    color="C1", alpha=.2,
    transform=ax.transAxes, clip_on=False,
)
ax.add_artist(rect)
ax.text(
    x=rect.get_width() / 2, y=1 + rect.get_height() / 2,
    s="Diamonds: very sparkly!", size=12,
    ha="center", va="center", transform=ax.transAxes,
)

res
```
Matplotlib 3.4 introduced the concept of :meth:`matplotlib.figure.Figure.subfigures`, which make it easier to composite multiple arrangements of subplots. These can also be passed to :meth:`Plot.on`, 

```python
f = mpl.figure.Figure(figsize=(7, 4), dpi=100, layout="constrained")
sf1, sf2 = f.subfigures(1, 2)

p.on(sf1).plot()
(
    so.Plot(diamonds, x="price")
    .add(so.Bars(), so.Hist())
    .facet(row="cut")
    .scale(x="log")
    .share(y=False)
    .on(sf2)
)
```


```python

```
