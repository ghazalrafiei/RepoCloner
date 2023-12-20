.. _objects_tutorial:

.. currentmodule:: seaborn.objects

The seaborn.objects interface
=============================

The `seaborn.objects` namespace was introduced in version 0.12 as a completely new interface for making seaborn plots. It offers a more consistent and flexible API, comprising a collection of composable classes for transforming and plotting data. In contrast to the existing `seaborn` functions, the new interface aims to support end-to-end plot specification and customization without dropping down to matplotlib (although it will remain possible to do so if necessary).

.. note::
    The objects interface is currently experimental and incomplete. It is stable enough for serious use, but there certainly are some rough edges and missing features.

```python
import seaborn as sns
import matplotlib as mpl
tips = sns.load_dataset("tips")
penguins = sns.load_dataset("penguins").dropna()
diamonds = sns.load_dataset("diamonds")
healthexp = sns.load_dataset("healthexp").sort_values(["Country", "Year"]).query("Year <= 2020")
```
Specifying a plot and mapping data
----------------------------------

The objects interface should be imported with the following convention:

```python
import seaborn.objects as so
```
The `seaborn.objects` namespace will provide access to all of the relevant classes. The most important is :class:`Plot`. You specify plots by instantiating a :class:`Plot` object and calling its methods. Let's see a simple example:

```python
(
    so.Plot(penguins, x="bill_length_mm", y="bill_depth_mm")
    .add(so.Dot())
)
```
This code, which produces a scatter plot, should look reasonably familiar. Just as when using :func:`seaborn.scatterplot`, we passed a tidy dataframe (`penguins`) and assigned two of its columns to the `x` and `y` coordinates of the plot. But instead of starting with the type of chart and then adding some data assignments, here we started with the data assignments and then added a graphical element.

Setting properties
~~~~~~~~~~~~~~~~~~

The :class:`Dot` class is an example of a :class:`Mark`: an object that graphically represents data values. Each mark will have a number of properties that can be set to change its appearance:

```python
(
    so.Plot(penguins, x="bill_length_mm", y="bill_depth_mm")
    .add(so.Dot(color="g", pointsize=4))
)
```
Mapping properties
~~~~~~~~~~~~~~~~~~

As with seaborn's functions, it is also possible to *map* data values to various graphical properties:

```python
(
    so.Plot(
        penguins, x="bill_length_mm", y="bill_depth_mm",
        color="species", pointsize="body_mass_g",
    )
    .add(so.Dot())
)
```
While this basic functionality is not novel, an important difference from the function API is that properties are mapped using the same parameter names that would set them directly (instead of having `hue` vs. `color`, etc.). What matters is *where* the property is defined: passing a value when you initialize :class:`Dot` will set it directly, whereas assigning a variable when you set up the :class:`Plot` will *map* the corresponding data.

Beyond this difference, the objects interface also allows a much wider range of mark properties to be mapped:

```python
(
    so.Plot(
        penguins, x="bill_length_mm", y="bill_depth_mm",
        edgecolor="sex", edgewidth="body_mass_g",
    )
    .add(so.Dot(color=".8"))
)
```
Defining groups
~~~~~~~~~~~~~~~

The :class:`Dot` mark represents each data point independently, so the assignment of a variable to a property only has the effect of changing each dot's appearance. For marks that group or connect observations, such as :class:`Line`, it also determines the number of distinct graphical elements:

```python
(
    so.Plot(healthexp, x="Year", y="Life_Expectancy", color="Country")
    .add(so.Line())
)
```
It is also possible to define a grouping without changing any visual properties, by using `group`:

```python
(
    so.Plot(healthexp, x="Year", y="Life_Expectancy", group="Country")
    .add(so.Line())
)
```
Transforming data before plotting
---------------------------------

Statistical transformation
~~~~~~~~~~~~~~~~~~~~~~~~~~

As with many seaborn functions, the objects interface supports statistical transformations. These are performed by :class:`Stat` objects, such as :class:`Agg`:

```python
(
    so.Plot(penguins, x="species", y="body_mass_g")
    .add(so.Bar(), so.Agg())
)
```
In the function interface, statistical transformations are possible with some visual representations (e.g. :func:`seaborn.barplot`) but not others (e.g. :func:`seaborn.scatterplot`). The objects interface more cleanly separates representation and transformation, allowing you to compose :class:`Mark` and :class:`Stat` objects:

```python
(
    so.Plot(penguins, x="species", y="body_mass_g")
    .add(so.Dot(pointsize=10), so.Agg())
)
```
When forming groups by mapping properties, the :class:`Stat` transformation is applied to each group separately:

```python
(
    so.Plot(penguins, x="species", y="body_mass_g", color="sex")
    .add(so.Dot(pointsize=10), so.Agg())
)
```
Resolving overplotting
~~~~~~~~~~~~~~~~~~~~~~

Some seaborn functions also have mechanisms that automatically resolve overplotting, as when :func:`seaborn.barplot` "dodges" bars once `hue` is assigned. The objects interface has less complex default behavior. Bars representing multiple groups will overlap by default:

```python
(
    so.Plot(penguins, x="species", y="body_mass_g", color="sex")
    .add(so.Bar(), so.Agg())
)
```
Nevertheless, it is possible to compose the :class:`Bar` mark with the :class:`Agg` stat and a second transformation, implemented by :class:`Dodge`:

```python
(
    so.Plot(penguins, x="species", y="body_mass_g", color="sex")
    .add(so.Bar(), so.Agg(), so.Dodge())
)
```
The :class:`Dodge` class is an example of a :class:`Move` transformation, which is like a :class:`Stat` but only adjusts `x` and `y` coordinates. The :class:`Move` classes can be applied with any mark, and it's not necessary to use a :class:`Stat` first:

```python
(
    so.Plot(penguins, x="species", y="body_mass_g", color="sex")
    .add(so.Dot(), so.Dodge())
)
```
It's also possible to apply multiple :class:`Move` operations in sequence:

```python
(
    so.Plot(penguins, x="species", y="body_mass_g", color="sex")
    .add(so.Dot(), so.Dodge(), so.Jitter(.3))
)
```
Creating variables through transformation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :class:`Agg` stat requires both `x` and `y` to already be defined, but variables can also be *created* through statistical transformation. For example, the :class:`Hist` stat requires only one of `x` *or* `y` to be defined, and it will create the other by counting observations:

```python
(
    so.Plot(penguins, x="species")
    .add(so.Bar(), so.Hist())
)
```
The :class:`Hist` stat will also create new `x` values (by binning) when given numeric data:

```python
(
    so.Plot(penguins, x="flipper_length_mm")
    .add(so.Bars(), so.Hist())
)
```
Notice how we used :class:`Bars`, rather than :class:`Bar` for the plot with the continuous `x` axis. These two marks are related, but :class:`Bars` has different defaults and works better for continuous histograms. It also produces a different, more efficient matplotlib artist. You will find the pattern of singular/plural marks elsewhere. The plural version is typically optimized for cases with larger numbers of marks.

Some transforms accept both `x` and `y`, but add *interval* data for each coordinate. This is particularly relevant for plotting error bars after aggregating:

```python
(
    so.Plot(penguins, x="body_mass_g", y="species", color="sex")
    .add(so.Range(), so.Est(errorbar="sd"), so.Dodge())
    .add(so.Dot(), so.Agg(), so.Dodge())
)
```
Orienting marks and transforms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When aggregating, dodging, and drawing a bar, the `x` and `y` variables are treated differently. Each operation has the concept of an *orientation*. The :class:`Plot` tries to determine the orientation automatically based on the data types of the variables. For instance, if we flip the assignment of `species` and `body_mass_g`, we'll get the same plot, but oriented horizontally:

```python
(
    so.Plot(penguins, x="body_mass_g", y="species", color="sex")
    .add(so.Bar(), so.Agg(), so.Dodge())
)
```
Sometimes, the correct orientation is ambiguous, as when both the `x` and `y` variables are numeric. In these cases, you can be explicit by passing the `orient` parameter to :meth:`Plot.add`:

```python
(
    so.Plot(tips, x="total_bill", y="size", color="time")
    .add(so.Bar(), so.Agg(), so.Dodge(), orient="y")
)
```
Building and displaying the plot
--------------------------------

Most examples this far have produced a single subplot with just one kind of mark on it. But :class:`Plot` does not limit you to this.

Adding multiple layers
~~~~~~~~~~~~~~~~~~~~~~

More complex single-subplot graphics can be created by calling :meth:`Plot.add` repeatedly. Each time it is called, it defines a *layer* in the plot. For example, we may want to add a scatterplot (now using :class:`Dots`) and then a regression fit:

```python
(
    so.Plot(tips, x="total_bill", y="tip")
    .add(so.Dots())
    .add(so.Line(), so.PolyFit())
)
```
Variable mappings that are defined in the :class:`Plot` constructor will be used for all layers:

```python
(
    so.Plot(tips, x="total_bill", y="tip", color="time")
    .add(so.Dots())
    .add(so.Line(), so.PolyFit())
)
```
Layer-specific mappings
~~~~~~~~~~~~~~~~~~~~~~~

You can also define a mapping such that it is used only in a specific layer. This is accomplished by defining the mapping within the call to :class:`Plot.add` for the relevant layer:

```python
(
    so.Plot(tips, x="total_bill", y="tip")
    .add(so.Dots(), color="time")
    .add(so.Line(color=".2"), so.PolyFit())
)
```
Alternatively, define the layer for the entire plot, but *remove* it from a specific layer by setting the variable to `None`:

```python
(
    so.Plot(tips, x="total_bill", y="tip", color="time")
    .add(so.Dots())
    .add(so.Line(color=".2"), so.PolyFit(), color=None)
)
```
To recap, there are three ways to specify the value of a mark property: (1) by mapping a variable in all layers, (2) by mapping a variable in a specific layer, and (3) by setting the property directly:

```python
from io import StringIO
from IPython.display import SVG
C = sns.color_palette("deep")
f = mpl.figure.Figure(figsize=(7, 3))
ax = f.subplots()
fontsize = 18
ax.add_artist(mpl.patches.Rectangle((.13, .53), .45, .09, color=C[0], alpha=.3))
ax.add_artist(mpl.patches.Rectangle((.22, .43), .235, .09, color=C[1], alpha=.3))
ax.add_artist(mpl.patches.Rectangle((.49, .43), .26, .09, color=C[2], alpha=.3))
ax.text(.05, .55, "Plot(data, 'x', 'y', color='var1')", size=fontsize, color=".2")
ax.text(.05, .45, ".add(Dot(pointsize=10), marker='var2')", size=fontsize, color=".2")
annots = [
    ("Mapped\nin all layers", (.35, .65), (0, 45)),
    ("Set directly", (.35, .4), (0, -45)),
    ("Mapped\nin this layer", (.63, .4), (0, -45)),
]
for i, (text, xy, xytext) in enumerate(annots):
    ax.annotate(
        text, xy, xytext,
        textcoords="offset points", fontsize=14, ha="center", va="center",
        arrowprops=dict(arrowstyle="->", color=C[i]), color=C[i],
    )
ax.set_axis_off()
f.subplots_adjust(0, 0, 1, 1)
f.savefig(s:=StringIO(), format="svg")
SVG(s.getvalue())
```
Faceting and pairing subplots
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As with seaborn's figure-level functions (:func:`seaborn.displot`, :func:`seaborn.catplot`, etc.), the :class:`Plot` interface can also produce figures with multiple "facets", or subplots containing subsets of data. This is accomplished with the :meth:`Plot.facet` method:

```python
(
    so.Plot(penguins, x="flipper_length_mm")
    .facet("species")
    .add(so.Bars(), so.Hist())
)
```
Call :meth:`Plot.facet` with the variables that should be used to define the columns and/or rows of the plot:

```python
(
    so.Plot(penguins, x="flipper_length_mm")
    .facet(col="species", row="sex")
    .add(so.Bars(), so.Hist())
)
```
You can facet using a variable with a larger number of levels by "wrapping" across the other dimension:

```python
(
    so.Plot(healthexp, x="Year", y="Life_Expectancy")
    .facet(col="Country", wrap=3)
    .add(so.Line())
)
```

All layers will be faceted unless you explicitly exclude them, which can be useful for providing additional context on each subplot:


```python
(
    so.Plot(healthexp, x="Year", y="Life_Expectancy")
    .facet("Country", wrap=3)
    .add(so.Line(alpha=.3), group="Country", col=None)
    .add(so.Line(linewidth=3))
)
```
An alternate way to produce subplots is :meth:`Plot.pair`. Like :class:`seaborn.PairGrid`, this draws all of the data on each subplot, using different variables for the x and/or y coordinates:

```python
(
    so.Plot(penguins, y="body_mass_g", color="species")
    .pair(x=["bill_length_mm", "bill_depth_mm"])
    .add(so.Dots())
)
```
You can combine faceting and pairing so long as the operations add subplots on opposite dimensions:

```python
(
    so.Plot(penguins, y="body_mass_g", color="species")
    .pair(x=["bill_length_mm", "bill_depth_mm"])
    .facet(row="sex")
    .add(so.Dots())
)
```
Integrating with matplotlib
~~~~~~~~~~~~~~~~~~~~~~~~~~~

There may be cases where you want multiple subplots to appear in a figure with a more complex structure than what :meth:`Plot.facet` or :meth:`Plot.pair` can provide. The current solution is to delegate figure setup to matplotlib and to supply the matplotlib object that :class:`Plot` should use with the :meth:`Plot.on` method. This object can be either a :class:`matplotlib.axes.Axes`, :class:`matplotlib.figure.Figure`, or :class:`matplotlib.figure.SubFigure`; the latter is most useful for constructing bespoke subplot layouts:

```python
f = mpl.figure.Figure(figsize=(8, 4))
sf1, sf2 = f.subfigures(1, 2)
(
    so.Plot(penguins, x="body_mass_g", y="flipper_length_mm")
    .add(so.Dots())
    .on(sf1)
    .plot()
)
(
    so.Plot(penguins, x="body_mass_g")
    .facet(row="sex")
    .add(so.Bars(), so.Hist())
    .on(sf2)
    .plot()
)
```
Building and displaying the plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An important thing to know is that :class:`Plot` methods clone the object they are called on and return that clone instead of updating the object in place. This means that you can define a common plot spec and then produce several variations on it.

So, take this basic specification:

```python
p = so.Plot(healthexp, "Year", "Spending_USD", color="Country")
```
We could use it to draw a line plot:

```python
p.add(so.Line())
```
Or perhaps a stacked area plot:

```python
p.add(so.Area(), so.Stack())
```
The :class:`Plot` methods are fully declarative. Calling them updates the plot spec, but it doesn't actually do any plotting. One consequence of this is that methods can be called in any order, and many of them can be called multiple times.

When does the plot actually get rendered? :class:`Plot` is optimized for use in notebook environments. The rendering is automatically triggered when the :class:`Plot` gets displayed in the Jupyter REPL. That's why we didn't see anything in the example above, where we defined a :class:`Plot` but assigned it to `p` rather than letting it return out to the REPL.

To see a plot in a notebook, either return it from the final line of a cell or call Jupyter's built-in `display` function on the object. The notebook integration bypasses :mod:`matplotlib.pyplot` entirely, but you can use its figure-display machinery in other contexts by calling :meth:`Plot.show`.

You can also save the plot to a file (or buffer) by calling :meth:`Plot.save`.Customizing the appearance
--------------------------

The new interface aims to support a deep amount of customization through :class:`Plot`, reducing the need to switch gears and use matplotlib functionality directly. (But please be patient; not all of the features needed to achieve this goal have been implemented!)

Parameterizing scales
~~~~~~~~~~~~~~~~~~~~~

All of the data-dependent properties are controlled by the concept of a :class:`Scale` and the :meth:`Plot.scale` method. This method accepts several different types of arguments. One possibility, which is closest to the use of scales in matplotlib, is to pass the name of a function that transforms the coordinates:

```python
(
    so.Plot(diamonds, x="carat", y="price")
    .add(so.Dots())
    .scale(y="log")
)
```
:meth:`Plot.scale` can also control the mappings for semantic properties like `color`. You can directly pass it any argument that you would pass to the `palette` parameter in seaborn's function interface:

```python
(
    so.Plot(diamonds, x="carat", y="price", color="clarity")
    .add(so.Dots())
    .scale(color="flare")
)
```
Another option is to provide a tuple of `(min, max)` values, controlling the range that the scale should map into. This works both for numeric properties and for colors:

```python
(
    so.Plot(diamonds, x="carat", y="price", color="clarity", pointsize="carat")
    .add(so.Dots())
    .scale(color=("#88c", "#555"), pointsize=(2, 10))
)
```
For additional control, you can pass a :class:`Scale` object. There are several different types of :class:`Scale`, each with appropriate parameters. For example, :class:`Continuous` lets you define the input domain (`norm`), the output range (`values`), and the function that maps between them (`trans`), while :class:`Nominal` allows you to specify an ordering:

```python
(
    so.Plot(diamonds, x="carat", y="price", color="carat", marker="cut")
    .add(so.Dots())
    .scale(
        color=so.Continuous("crest", norm=(0, 3), trans="sqrt"),
        marker=so.Nominal(["o", "+", "x"], order=["Ideal", "Premium", "Good"]),
    )
)
```
Customizing legends and ticks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :class:`Scale` objects are also how you specify which values should appear as tick labels / in the legend, along with how they appear. For example, the :meth:`Continuous.tick` method lets you control the density or locations of the ticks, and the :meth:`Continuous.label` method lets you modify the format:

```python
(
    so.Plot(diamonds, x="carat", y="price", color="carat")
    .add(so.Dots())
    .scale(
        x=so.Continuous().tick(every=0.5),
        y=so.Continuous().label(like="${x:.0f}"),
        color=so.Continuous().tick(at=[1, 2, 3, 4]),
    )
)
```
Customizing limits, labels, and titles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:class:`Plot` has a number of methods for simple customization, including :meth:`Plot.label`, :meth:`Plot.limit`, and :meth:`Plot.share`:

```python
(
    so.Plot(penguins, x="body_mass_g", y="species", color="island")
    .facet(col="sex")
    .add(so.Dot(), so.Jitter(.5))
    .share(x=False)
    .limit(y=(2.5, -.5))
    .label(
        x="Body mass (g)", y="",
        color=str.capitalize,
        title="{} penguins".format,
    )
)
```
Theme customization
~~~~~~~~~~~~~~~~~~~

Finally, :class:`Plot` supports data-independent theming through the :class:`Plot.theme` method. Currently, this method accepts a dictionary of matplotlib rc parameters. You can set them directly and/or pass a package of parameters from seaborn's theming functions:

```python
from seaborn import axes_style
theme_dict = {**axes_style("whitegrid"), "grid.linestyle": ":"}
so.Plot().theme(theme_dict)
```
To change the theme for all :class:`Plot` instances, update the settings in :attr:`Plot.config`:

```python
so.Plot.config.theme.update(theme_dict)
```
