```python
import seaborn as sns
sns.set_theme(style="white")
```
In the simplest invocation, assign ``x`` and ``y`` to create a scatterplot (using :func:`scatterplot`) with marginal histograms (using :func:`histplot`):

```python
penguins = sns.load_dataset("penguins")
sns.jointplot(data=penguins, x="bill_length_mm", y="bill_depth_mm")
```
Assigning a ``hue`` variable will add conditional colors to the scatterplot and draw separate density curves (using :func:`kdeplot`) on the marginal axes:

```python
sns.jointplot(data=penguins, x="bill_length_mm", y="bill_depth_mm", hue="species")
```
Several different approaches to plotting are available through the ``kind`` parameter. Setting ``kind="kde"`` will draw both bivariate and univariate KDEs:

```python
sns.jointplot(data=penguins, x="bill_length_mm", y="bill_depth_mm", hue="species", kind="kde")
```
Set ``kind="reg"`` to add a linear regression fit (using :func:`regplot`) and univariate KDE curves:

```python
sns.jointplot(data=penguins, x="bill_length_mm", y="bill_depth_mm", kind="reg")
```
There are also two options for bin-based visualization of the joint distribution. The first, with ``kind="hist"``, uses :func:`histplot` on all of the axes:

```python
sns.jointplot(data=penguins, x="bill_length_mm", y="bill_depth_mm", kind="hist")
```
Alternatively, setting ``kind="hex"`` will use :meth:`matplotlib.axes.Axes.hexbin` to compute a bivariate histogram using hexagonal bins:

```python
sns.jointplot(data=penguins, x="bill_length_mm", y="bill_depth_mm", kind="hex")
```
Additional keyword arguments can be passed down to the underlying plots:

```python
sns.jointplot(
    data=penguins, x="bill_length_mm", y="bill_depth_mm",
    marker="+", s=100, marginal_kws=dict(bins=25, fill=False),
)
```
Use :class:`JointGrid` parameters to control the size and layout of the figure:

```python
sns.jointplot(data=penguins, x="bill_length_mm", y="bill_depth_mm", height=5, ratio=2, marginal_ticks=True)
```
To add more layers onto the plot, use the methods on the :class:`JointGrid` object that :func:`jointplot` returns:

```python
g = sns.jointplot(data=penguins, x="bill_length_mm", y="bill_depth_mm")
g.plot_joint(sns.kdeplot, color="r", zorder=0, levels=6)
g.plot_marginals(sns.rugplot, color="r", height=-.15, clip_on=False)
```
