```python
import seaborn.objects as so
```
Theme configuration
^^^^^^^^^^^^^^^^^^^

Theme changes made through the the :attr:`Plot.config` interface will apply to all subsequent :class:`Plot` instances. Use the :meth:`Plot.theme` method to modify the theme on a plot-by-plot basis.

The theme is a dictionary of matplotlib `rc parameters <https://matplotlib.org/stable/tutorials/introductory/customizing.html>`_. You can set individual parameters directly:

```python
so.Plot.config.theme["axes.facecolor"] = "white"
```
To change the overall style of the plot, update the theme with a dictionary of parameters, perhaps from one of seaborn's theming functions:

```python
from seaborn import axes_style
so.Plot.config.theme.update(axes_style("whitegrid"))
```
To sync :class:`Plot` with matplotlib's global state, pass the `rcParams` dictionary:

```python
import matplotlib as mpl
so.Plot.config.theme.update(mpl.rcParams)
```
The theme can also be reset back to seaborn defaults:

```python
so.Plot.config.theme.reset()
```
Display configuration
^^^^^^^^^^^^^^^^^^^^^

When returned from the last statement in a notebook cell, a :class:`Plot` will be compiled and embedded in the notebook as an image. By default, the image is rendered as HiDPI PNG. Alternatively, it is possible to display the plots in SVG format:

```python
so.Plot.config.display["format"] = "svg"
```
SVG images use vector graphics with "infinite" resolution, so they will appear crisp at any amount of zoom. The downside is that each plot element is drawn separately, so the image data can get very heavy for certain kinds of plots (e.g., for dense scatterplots).

The HiDPI scaling of the default PNG images will also inflate the size of the notebook they are stored in. (Unlike with SVG, PNG size will scale with the dimensions of the plot but not its complexity). When not useful, it can be disabled:

```python
so.Plot.config.display["hidpi"] = False
```
The embedded images are scaled down slightly — independently from the figure size or DPI — so that more information can be presented on the screen. The precise scaling factor is also configurable:

```python
so.Plot.config.display["scaling"] = 0.7
```
