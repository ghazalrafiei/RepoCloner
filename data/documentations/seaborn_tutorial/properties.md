.. _properties_tutorial:

Properties of Mark objects
===========================

```python
import numpy as np
import pandas as pd
import matplotlib as mpl
import seaborn.objects as so
from seaborn import axes_style, color_palette
```
Coordinate properties
---------------------.. _coordinate_property:

x, y, xmin, xmax, ymin, ymax
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Coordinate properties determine where a mark is drawn on a plot. Canonically, the `x` coordinate is the horizontal position and the `y` coordinate is the vertical position. Some marks accept a span (i.e., `min`, `max`) parameterization for one or both variables. Others may accept `x` and `y` but also use a `baseline` parameter to show a span. The layer's `orient` parameter determines how this works.

If a variable does not contain numeric data, its scale will apply a conversion so that data can be drawn on a screen. For instance, :class:`Nominal` scales assign an integer index to each distinct category, and :class:`Temporal` scales represent dates as the number of days from a reference "epoch":

```python
(
    so.Plot(y=[0, 0, 0])
    .pair(x=[
        [1, 2, 3],
        ["A", "B", "C"],
        np.array(["2020-01-01", "2020-02-01", "2020-03-01"], dtype="datetime64"),
    ])
    .limit(
        x0=(0, 10),
        x1=(-.5, 2.5),
        x2=(pd.Timestamp("2020-01-01"), pd.Timestamp("2020-03-01"))
    )
    .scale(y=so.Continuous().tick(count=0), x2=so.Temporal().label(concise=True))
    .layout(size=(7, 1), engine="tight")
    .label(x0="Continuous", x1="Nominal", x2="Temporal")
    .theme({
        **axes_style("ticks"),
        **{f"axes.spines.{side}": False for side in ["left", "right", "top"]},
    })
)
```
A :class:`Continuous` scale can also apply a nonlinear transform between data values and spatial positions:

```python
(
    so.Plot(y=[0, 0, 0])
    .pair(x=[[1, 10, 100], [-100, 0, 100], [0, 10, 40]])
    .limit(
    )
    .add(so.Dot(marker=""))
    .scale(
        y=so.Continuous().tick(count=0),
        x0=so.Continuous(trans="log"),
        x1=so.Continuous(trans="symlog").tick(at=[-100, -10, 0, 10, 100]),
        x2=so.Continuous(trans="sqrt").tick(every=10),
    )
    .layout(size=(7, 1), engine="tight")
    .label(x0="trans='log'", x1="trans='symlog'", x2="trans='sqrt'")
    .theme({
        **axes_style("ticks"),
        **{f"axes.spines.{side}": False for side in ["left", "right", "top"]},
        "axes.labelpad": 8,
    })
)
```


```python
# Hiding from the page but keeping around for now
(
    so.Plot()
    .add(
        so.Dot(edgewidth=3, stroke=3),
        so.Dodge(by=["group"]),
        x=["A", "A", "A", "A", "A"],
        y=[1.75, 2.25, 2.75, 2.0, 2.5],
        color=[1, 2, 3, 1, 3],
        marker=[mpl.markers.MarkerStyle(x) for x in "os^+o"],
        pointsize=(9, 9, 9, 13, 10),
        fill=[True, False, True, True, False],
        group=[1, 2, 3, 4, 5], width=.5, legend=False,
    )
    .add(
        so.Bar(edgewidth=2.5, alpha=.2, width=.9),
        so.Dodge(gap=.05),
        x=["B", "B", "B",], y=[2, 2.5, 1.75], color=[1, 2, 3],
        legend=False,
    )
    .add(
        so.Range({"capstyle": "round"}, linewidth=3),
        so.Dodge(by=["group"]),
        x=["C", "C", "C"], ymin=[1.5, 1.75, 1.25], ymax=[2.5, 2.75, 2.25],
        color=[1, 2, 2], linestyle=["-", "-", ":"],
        group=[1, 2, 3], width=.5, legend=False,
    )
    .layout(size=(4, 4), engine=None)
    .limit(x=(-.5, 2.5), y=(0, 3))
    .label(x="X Axis (nominal)", y="Y Axis (continuous)")
    .scale(
        color="dark:C0_r", #None,
        fill=None, marker=None,
        pointsize=None, linestyle=None,
        y=so.Continuous().tick(every=1, minor=1)
    )
    .theme({
        **axes_style("ticks"),
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.labelsize": 14,
    })
)
```
Color properties
----------------.. _color_property:

color, fillcolor, edgecolor
~~~~~~~~~~~~~~~~~~~~~~~~~~~

All marks can be given a `color`, and many distinguish between the color of the mark's "edge" and "fill". Often, simply using `color` will set both, while the more-specific properties allow further control:

```python
no_spines = {
    f"axes.spines.{side}": False
    for side in ["left", "right", "bottom", "top"]
}
```


```python
color_mark = so.Dot(marker="s", pointsize=20, edgewidth=2.5, alpha=.7, edgealpha=1)
color_plot = (
    so.Plot()
    .theme({
        **axes_style("white"),
        **no_spines,
        "axes.titlesize": 15,
        "figure.subplot.wspace": .1,
        "axes.xmargin": .1,
    })
    .scale(
        x=so.Continuous().tick(count=0),
        y=so.Continuous().tick(count=0),
        color=None, edgecolor=None,
    )
    .layout(size=(9, .5), engine=None)
)
```


```python
n = 6
rgb = [f"C{i}" for i in range(n)]
(
    color_plot
    .facet(["color"] * n + ["edgecolor"] * n + ["fillcolor"] * n)
    .add(
        color_mark,
        x=np.tile(np.arange(n), 3),
        y=np.zeros(n * 3),
        color=rgb + [".8"] * n + rgb,
        edgecolor=rgb + rgb + [".3"] * n,
        legend=False,
    )
    .plot()
)
```
When the color property is mapped, the default palette depends on the type of scale. Nominal scales use discrete, unordered hues, while continuous scales (including temporal ones) use a sequential gradient:

```python
n = 9
rgb = color_palette("deep", n) + color_palette("ch:", n)
(
    color_plot
    .facet(["nominal"] * n + ["continuous"] * n)
    .add(
        color_mark,
        x=list(range(n)) * 2,
        y=[0] * n * 2,
        color=rgb,
        legend=False,
    )
    .plot()
)
```
.. note::
    The default continuous scale is subject to change in future releases to improve discriminability.

Color scales are parameterized by the name of a palette, such as `'viridis'`, `'rocket'`, or `'deep'`. Some palette names can include parameters, including simple gradients (e.g. `'dark:blue'`) or the cubehelix system (e.g. `'ch:start=.2,rot=-.4``). See the :doc:`color palette tutorial </tutorial/color_palettes>` for guidance on making an appropriate selection.

Continuous scales can also be parameterized by a tuple of colors that the scale should interpolate between. When using a nominal scale, it is possible to provide either the name of the palette (which will be discretely-sampled, if necessary), a list of individual color values, or a dictionary directly mapping data values to colors.

Individual colors may be specified `in a wide range of formats <https://matplotlib.org/stable/tutorials/colors/colors.html>`_. These include indexed references to the current color cycle (`'C0'`), single-letter shorthands (`'b'`), grayscale values (`'.4'`), RGB hex codes (`'#4c72b0'`), X11 color names (`'seagreen'`), and XKCD color survey names (`'purpleish'`):

```python
color_dict = {
    "cycle": ["C0", "C1", "C2"],
    "short": ["r", "y", "b"],
    "gray": [".3", ".7", ".5"],
    "hex": ["#825f87", "#05696b", "#de7e5d"],
    "X11": ["seagreen", "sienna", "darkblue"],
    "XKCD": ["xkcd:gold", "xkcd:steel", "xkcd:plum"],
}
groups = [k for k in color_dict for _ in range(3)]
colors = [c for pal in color_dict.values() for c in pal]
(
    so.Plot(
        x=[0] * len(colors),
        y=[f"'{c}'" for c in colors],
        color=colors,
    )
    .theme({
        **axes_style("ticks"),
        **no_spines,
        "axes.ymargin": .2,
        "axes.titlesize": 14,
        
    })
    .facet(groups)
    .layout(size=(8, 1.15), engine="constrained")
    .scale(x=so.Continuous().tick(count=0))
    .add(color_mark)
    .limit(x=(-.2, .5))
    # .label(title="{}      ".format)
    .label(title="")
    .scale(color=None)
    .share(y=False)
    .plot()
)
```
.. _alpha_property:

alpha, fillalpha, edgealpha
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `alpha` property determines the mark's opacity. Lowering the alpha can be helpful for representing density in the case of overplotting:

```python
rng = np.random.default_rng(3)
n_samp = 300
x = 1 - rng.exponential(size=n_samp)
y = rng.uniform(-1, 1, size=n_samp)
keep = np.sqrt(x ** 2 + y ** 2) < 1
x, y = x[keep], y[keep]
n = keep.sum()
alpha_vals = np.linspace(.1, .9, 9).round(1)
xs = np.concatenate([x for _ in alpha_vals])
ys = np.concatenate([y for _ in alpha_vals])
alphas = np.repeat(alpha_vals, n)
(
    so.Plot(x=xs, y=ys, alpha=alphas)
    .facet(alphas)
    .add(so.Dot(color=".2", pointsize=3))
    .scale(
        alpha=None,
        x=so.Continuous().tick(count=0),
        y=so.Continuous().tick(count=0)
    )
    .layout(size=(9, 1), engine=None)
    .theme({
        **axes_style("white"),
        **no_spines,
    })
)
```
Mapping the `alpha` property can also be useful even when marks do not overlap because it conveys a sense of importance and can be combined with a `color` scale to represent two variables. Moreover, colors with lower alpha appear less saturated, which can improve the appearance of larger filled marks (such as bars).

As with `color`, some marks define separate `edgealpha` and `fillalpha` properties for additional control.Style properties
----------------.. _fill_property:

fill
~~~~

The `fill` property is relevant to marks with a distinction between the edge and interior and determines whether the interior is visible. It is a boolean state: `fill` can be set only to `True` or `False`:

```python
nan = float("nan")
x_bar = [0, 1]
y_bar = [2, 1]
f_bar = [True, False]

x_dot = [2.2, 2.5, 2.8, 3.2, 3.5, 3.8]
y_dot = [1.2, 1.7, 1.4, 0.7, 1.2, 0.9]
f_dot = [True, True, True, False, False, False]

xx = np.linspace(0, .8, 100)
yy = xx ** 2 * np.exp(-xx * 10)
x_area = list(4.5 + xx) + list(5.5 + xx)
y_area = list(yy / yy.max() * 2) + list(yy / yy.max())
f_area = [True] * 100 + [False] * 100

(
    so.Plot()
    .add(
        so.Bar(color=".3", edgecolor=".2", edgewidth=2.5),
        x=x_bar + [nan for _ in x_dot + x_area],
        y=y_bar + [nan for _ in y_dot + y_area],
        fill=f_bar + [nan for _ in f_dot + f_area]
    )
    .add(
        so.Dot(color=".2", pointsize=13, stroke=2.5),
        x=[nan for _ in x_bar] + x_dot + [nan for _ in x_area],
        y=[nan for _ in y_bar] + y_dot + [nan for _ in y_area],
        fill=[nan for _ in f_bar] + f_dot + [nan for _ in f_area],
    )
    .add(
        so.Area(color=".2", edgewidth=2.5),
        x=[nan for _ in x_bar + x_dot] + x_area,
        y=[nan for _ in y_bar + y_dot] + y_area,
        fill=[nan for _ in f_bar + f_dot] + f_area,
    )
    .theme({
        **axes_style("ticks"),
        "axes.spines.left": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.labelsize": 14,
    })
    .layout(size=(9, 1.25), engine=None)
    .scale(
        fill=None,
        x=so.Continuous().tick(at=[0, 1, 2.5, 3.5, 4.8, 5.8]).label(
            like={
                0: True, 1: False, 2.5: True, 3.5: False, 4.8: True, 5.8: False
            }.get,
        ),
        y=so.Continuous().tick(count=0),
    )
)
```
.. _marker_property:

marker
~~~~~~

The `marker` property is relevant for dot marks and some line marks. The API for specifying markers is very flexible, as detailed in the matplotlib API docs: :mod:`matplotlib.markers`.

```python
marker_plot = (
    so.Plot()
    .scale(marker=None, y=so.Continuous().tick(count=0))
    .layout(size=(10, .5), engine=None)
    .theme({
        **axes_style("ticks"),
        "axes.spines.left": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.labelsize":12,
        "axes.xmargin": .02,
    })

)
marker_mark = so.Dot(pointsize=15, color=".2", stroke=1.5)
```
Markers can be specified using a number of simple string codes:

```python
marker_codes = [
    "o", "^", "v", "<", ">","s", "D", "d", "p", "h", "H", "8",
    "X", "*", ".", "P", "x", "+", "1", "2", "3", "4", "|", "_",
]
x, y = [f"'{m}'" for m in marker_codes], [0] * len(marker_codes)
marker_objs = [mpl.markers.MarkerStyle(m) for m in marker_codes]
marker_plot.add(marker_mark, marker=marker_objs, x=x, y=y).plot()
```
They can also be programatically generated using a `(num_sides, fill_style, angle)` tuple:

```python
marker_codes = [
    (4, 0, 0), (4, 0, 45), (8, 0, 0),
    (4, 1, 0), (4, 1, 45), (8, 1, 0),
    (4, 2, 0), (4, 2, 45), (8, 2, 0),
]
x, y = [f"{m}" for m in marker_codes], [0] * len(marker_codes)
marker_objs = [mpl.markers.MarkerStyle(m) for m in marker_codes]
marker_plot.add(marker_mark, marker=marker_objs, x=x, y=y).plot()
```
See the matplotlib docs for additional formats, including mathtex character codes (`'$...$'`) and arrays of vertices.

A marker property is always mapped with a nominal scale; there is no inherent ordering to the different shapes. If no scale is provided, the plot will programmatically generate a suitably large set of unique markers:

```python
from seaborn._core.properties import Marker
n = 14
marker_objs = Marker()._default_values(n)
x, y = list(map(str, range(n))), [0] * n
marker_plot.add(marker_mark, marker=marker_objs, x=x, y=y).plot()
```
While this ensures that the shapes are technically distinct, bear in mind that — in most cases — it will be difficult to tell the markers apart if more than a handful are used in a single plot.

.. note::
    The default marker scale is subject to change in future releases to improve discriminability... _linestyle_property:

linestyle, edgestyle
~~~~~~~~~~~~~~~~~~~~

The `linestyle` property is relevant to line marks, and the `edgestyle` property is relevant to a number of marks with "edges. Both properties determine the "dashing" of a line in terms of on-off segments.

Dashes can be specified with a small number of shorthand codes (`'-'`, `'--'`, `'-.'`, and `':'`) or programatically using `(on, off, ...)` tuples. In the tuple specification, the unit is equal to the linewidth:

```python
xx = np.linspace(0, 1, 100)
dashes = ["-", "--", "-.", ":", (6, 2), (2, 1), (.5, .5), (4, 1, 2, 1)] 
dash_data = (
    pd.DataFrame({i: xx for i in range(len(dashes))})
    .stack()
    .reset_index(1)
    .set_axis(["y", "x"], axis=1)
    .reset_index(drop=True)
)
(
    so.Plot(dash_data, "x", "y", linestyle="y")
    .add(so.Line(linewidth=1.7, color=".2"), legend=None)
    .scale(
        linestyle=dashes,
        x=so.Continuous().tick(count=0),
        y=so.Continuous().tick(every=1).label(like={
            i: f"'$\mathtt{{{pat}}}$'" if isinstance(pat, str) else pat
            for i, pat in enumerate(dashes)
        }.get)
    )
    .label(x="", y="")
    .limit(x=(0, 1), y=(7.5, -0.5))
    .layout(size=(9, 2.5), engine=None)
    .theme({
        **axes_style("white"),
        **no_spines,
        "ytick.labelsize": 12,
    })
)
```
Size properties
---------------.. _pointsize_property:

pointsize
~~~~~~~~~

The `pointsize` property is relevant to dot marks and to line marks that can show markers at individual data points. The units correspond to the diameter of the mark in points.

Note that, while the parameterization corresponds to diameter, scales will be applied with a square root transform so that data values are linearly proportional to area:

```python
x = np.arange(1, 21)
y = [0 for _ in x]
(
    so.Plot(x, y)
    .add(so.Dots(color=".2", stroke=1), pointsize=x)
    .layout(size=(9, .5), engine=None)
    .theme({
        **axes_style("ticks"),
        **{f"axes.spines.{side}": False for side in ["left", "right", "top"]},
        "xtick.labelsize": 12,
        "axes.xmargin": .025,
    })
    .scale(
        pointsize=None,
        x=so.Continuous().tick(every=1),
        y=so.Continuous().tick(count=0),
    )
)
```
.. _linewidth_property:

linewidth
~~~~~~~~~

The `linewidth` property is relevant to line marks and determines their thickness. The value should be non-negative and has point units:

```python
lw = np.arange(0.5, 5, .5)
x = [i for i in [0, 1] for _ in lw]
y = [*lw, *lw]
(
    so.Plot(x=x, y=y, linewidth=y)
    .add(so.Line(color=".2"))
    .limit(y=(4.9, .1))
    .layout(size=(9, 1.4), engine=None)
    .theme({
        **axes_style("ticks"),
        **{f"axes.spines.{side}": False for side in ["bottom", "right", "top"]},
        "xtick.labelsize": 12,
        "axes.xmargin": .015,
        "ytick.labelsize": 12,
    })
    .scale(
        linewidth=None,
        x=so.Continuous().tick(count=0),
        y=so.Continuous().tick(every=1, between=(.5, 4.5), minor=1),
    )
)
```
.. _edgewidth_property:

edgewidth
~~~~~~~~~

The `edgewidth` property is akin to `linewidth` but applies to marks with an edge/fill rather than to lines. It also has a different default range when used in a scale. The units are the same:

```python
x = np.arange(0, 21) / 5
y = [0 for _ in x]
edge_plot = (
    so.Plot(x, y)
    .layout(size=(9, .5), engine=None)
    .theme({
        **axes_style("ticks"),
        **{f"axes.spines.{side}": False for side in ["left", "right", "top"]},
        "xtick.labelsize": 12,
        "axes.xmargin": .02,
    })
    .scale(
        x=so.Continuous().tick(every=1, minor=4),
        y=so.Continuous().tick(count=0),
    )
)
```


```python
(
    edge_plot
    .add(so.Dot(color=".75", edgecolor=".2", marker="o", pointsize=14), edgewidth=x)
    .scale(edgewidth=None)
    .plot()
)
```
.. _stroke_property:

stroke
~~~~~~

The `stroke` property is akin to `edgewidth` but applies when a dot mark is defined by its stroke rather than its fill. It also has a slightly different default scale range, but otherwise behaves similarly:

```python
(
    edge_plot
    .add(so.Dot(color=".2", marker="x", pointsize=11), stroke=x)
    .scale(stroke=None)
    .plot()
)
```
Text properties
---------------.. _horizontalalignment_property:

.. _verticalalignment_property:

halign, valign
~~~~~~~~~~~~~~

The `halign` and `valign` properties control the *horizontal* and *vertical* alignment of text marks. The options for horizontal alignment are `'left'`, `'right'`, and `'center'`, while the options for vertical alignment are `'top'`, `'bottom'`, `'center'`, `'baseline'`, and `'center_baseline'`.

```python
x = ["left", "right", "top", "bottom", "baseline", "center"]
ha = x[:2] + ["center"] * 4
va = ["center_baseline"] * 2 + x[2:]
y = np.zeros(len(x))
(
    so.Plot(x=[f"'{_x_}'" for _x_ in x], y=y, halign=ha, valign=va)
    .add(so.Dot(marker="+", color="r", alpha=.5, stroke=1, pointsize=24))
    .add(so.Text(text="XyZ", fontsize=14, offset=0))
    .scale(y=so.Continuous().tick(at=[]), halign=None, valign=None)
    .limit(x=(-.25, len(x) - .75))
    .layout(size=(9, .6), engine=None)
    .theme({
        **axes_style("ticks"),
        **{f"axes.spines.{side}": False for side in ["left", "right", "top"]},
        "xtick.labelsize": 12,
        "axes.xmargin": .015,
        "ytick.labelsize": 12,
    })
    .plot()
)
```
.. _fontsize_property:

fontsize
~~~~~~~~

The `fontsize` property controls the size of textual marks. The value has point units:

```python
from string import ascii_uppercase
n = 26
s = np.arange(n) + 1
y = np.zeros(n)
t = list(ascii_uppercase[:n])
(
    so.Plot(x=s, y=y, text=t, fontsize=s)
    .add(so.Text())
    .scale(x=so.Nominal(), y=so.Continuous().tick(at=[]))
    .layout(size=(9, .5), engine=None)
    .theme({
        **axes_style("ticks"),
        **{f"axes.spines.{side}": False for side in ["left", "right", "top"]},
        "xtick.labelsize": 12,
        "axes.xmargin": .015,
        "ytick.labelsize": 12,
    })
    .plot()
)
```
.. _offset_property:

offset
~~~~~~

The `offset` property controls the spacing between a text mark and its anchor position. It applies when *not* using `center` alignment (i.e., when using left/right or top/bottom). The value has point units. 

```python
n = 17
x = np.linspace(0, 8, n)
y = np.full(n, .5)
(
    so.Plot(x=x, y=y, offset=x)
    .add(so.Bar(color=".6", edgecolor="k"))
    .add(so.Text(text="abc", valign="bottom"))
    .scale(
        x=so.Continuous().tick(every=1, minor=1),
        y=so.Continuous().tick(at=[]),
        offset=None,
    )
    .limit(y=(0, 1.5))
    .layout(size=(9, .5), engine=None)
    .theme({
        **axes_style("ticks"),
        **{f"axes.spines.{side}": False for side in ["left", "right", "top"]},
        "axes.xmargin": .015,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
    })
    .plot()
)
```
Other properties
----------------.. _property_property:

text
~~~~

The `text` property is used to set the content of a textual mark. It is always used literally (not mapped), and cast to string when necessary.

group
~~~~~

The `group` property is special in that it does not change anything about the mark's appearance but defines additional data subsets that transforms should operate on independently.

```python

```
