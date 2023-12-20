```python
import seaborn as sns
sns.set_theme(style="ticks")
```
The simplest invocation uses :func:`scatterplot` for each pairing of the variables and :func:`histplot` for the marginal plots along the diagonal:

```python
penguins = sns.load_dataset("penguins")
sns.pairplot(penguins)
```
Assigning a ``hue`` variable adds a semantic mapping and changes the default marginal plot to a layered kernel density estimate (KDE):

```python
sns.pairplot(penguins, hue="species")
```
It's possible to force marginal histograms:

```python
sns.pairplot(penguins, hue="species", diag_kind="hist")
```
The ``kind`` parameter determines both the diagonal and off-diagonal plotting style. Several options are available, including using :func:`kdeplot` to draw KDEs:

```python
sns.pairplot(penguins, kind="kde")
```
Or :func:`histplot` to draw both bivariate and univariate histograms:

```python
sns.pairplot(penguins, kind="hist")
```
The ``markers`` parameter applies a style mapping on the off-diagonal axes. Currently, it will be redundant with the ``hue`` variable:

```python
sns.pairplot(penguins, hue="species", markers=["o", "s", "D"])
```
As with other figure-level functions, the size of the figure is controlled by setting the ``height`` of each individual subplot:

```python
sns.pairplot(penguins, height=1.5)
```
Use ``vars`` or ``x_vars`` and ``y_vars`` to select the variables to plot:

```python
sns.pairplot(
    penguins,
    x_vars=["bill_length_mm", "bill_depth_mm", "flipper_length_mm"],
    y_vars=["bill_length_mm", "bill_depth_mm"],
)
```
Set ``corner=True`` to plot only the lower triangle:

```python
sns.pairplot(penguins, corner=True)
```
The ``plot_kws`` and ``diag_kws`` parameters accept dicts of keyword arguments to customize the off-diagonal and diagonal plots, respectively:

```python
sns.pairplot(
    penguins,
    plot_kws=dict(marker="+", linewidth=1),
    diag_kws=dict(fill=False),
)
```
The return object is the underlying :class:`PairGrid`, which can be used to further customize the plot:

```python
g = sns.pairplot(penguins, diag_kind="kde")
g.map_lower(sns.kdeplot, levels=4, color=".2")
```
