```python
import seaborn.objects as so
from seaborn import load_dataset
anscombe = load_dataset("anscombe")
```
The default theme uses the same parameters as :func:`seaborn.set_theme` with no additional arguments:

```python
p = (
    so.Plot(anscombe, "x", "y", color="dataset")
    .facet("dataset", wrap=2)
    .add(so.Line(), so.PolyFit(order=1))
    .add(so.Dot())
)
p
```
Pass a dictionary of rc parameters to change the appearance of the plot:

```python
p.theme({"axes.facecolor": "w", "axes.edgecolor": "slategray"})
```
Many (though not all) mark properties will reflect theme parameters by default:

```python
p.theme({"lines.linewidth": 4})
```
Apply seaborn styles by passing in the output of the style functions:

```python
from seaborn import axes_style
p.theme(axes_style("ticks"))
```
Or apply styles that ship with matplotlib:

```python
from matplotlib import style
p.theme(style.library["fivethirtyeight"])
```
Multiple parameter dictionaries should be passed to the same function call. On Python 3.9+, you can use dictionary union syntax for this:

```python
from seaborn import plotting_context
p.theme(axes_style("whitegrid") | plotting_context("talk"))
```
The default theme for all :class:`Plot` instances can be changed using the :attr:`Plot.config` attribute:

```python
so.Plot.config.theme.update(axes_style("white"))
p
```
See :ref:`Plot Configuration <plot_config>` for more details.