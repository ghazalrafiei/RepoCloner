```python
import seaborn as sns
sns.set_theme()
```
Calling the constructor initializes the figure, but it does not plot anything:

```python
penguins = sns.load_dataset("penguins")
sns.JointGrid(data=penguins, x="bill_length_mm", y="bill_depth_mm")
```
The simplest plotting method, :meth:`JointGrid.plot` accepts a pair of functions (one for the joint axes and one for both marginal axes):

```python
g = sns.JointGrid(data=penguins, x="bill_length_mm", y="bill_depth_mm")
g.plot(sns.scatterplot, sns.histplot)
```
The :meth:`JointGrid.plot` function also accepts additional keyword arguments, but it passes them to both functions:

```python
g = sns.JointGrid(data=penguins, x="bill_length_mm", y="bill_depth_mm")
g.plot(sns.scatterplot, sns.histplot, alpha=.7, edgecolor=".2", linewidth=.5)
```
If you need to pass different keyword arguments to each function, you'll have to invoke :meth:`JointGrid.plot_joint` and :meth:`JointGrid.plot_marginals`:

```python
g = sns.JointGrid(data=penguins, x="bill_length_mm", y="bill_depth_mm")
g.plot_joint(sns.scatterplot, s=100, alpha=.5)
g.plot_marginals(sns.histplot, kde=True)
```
You can also set up the grid without assigning any data:

```python
g = sns.JointGrid()
```
You can then plot by accessing the ``ax_joint``, ``ax_marg_x``, and ``ax_marg_y`` attributes, which are :class:`matplotlib.axes.Axes` objects:

```python
g = sns.JointGrid()
x, y = penguins["bill_length_mm"], penguins["bill_depth_mm"]
sns.scatterplot(x=x, y=y, ec="b", fc="none", s=100, linewidth=1.5, ax=g.ax_joint)
sns.histplot(x=x, fill=False, linewidth=2, ax=g.ax_marg_x)
sns.kdeplot(y=y, linewidth=2, ax=g.ax_marg_y)
```
The plotting methods can use any seaborn functions that accept ``x`` and ``y`` variables:

```python
g = sns.JointGrid(data=penguins, x="bill_length_mm", y="bill_depth_mm")
g.plot(sns.regplot, sns.boxplot)
```
If the functions accept a ``hue`` variable, you can use it by assigning ``hue`` when you call the constructor:

```python
g = sns.JointGrid(data=penguins, x="bill_length_mm", y="bill_depth_mm", hue="species")
g.plot(sns.scatterplot, sns.histplot)
```

Horizontal and/or vertical reference lines can be added to the joint and/or marginal axes using :meth:`JointGrid.refline`:


```python
g = sns.JointGrid(data=penguins, x="bill_length_mm", y="bill_depth_mm")
g.plot(sns.scatterplot, sns.histplot)
g.refline(x=45, y=16)
```
The figure will always be square (unless you resize it at the matplotlib layer), but its overall size and layout are configurable. The size is controlled by the ``height`` parameter. The relative ratio between the joint and marginal axes is controlled by ``ratio``, and the amount of space between the plots is controlled by ``space``:

```python
sns.JointGrid(height=4, ratio=2, space=.05)
```
By default, the ticks on the density axis of the marginal plots are turned off, but this is configurable:

```python
sns.JointGrid(marginal_ticks=True)
```
Limits on the two data axes (which are shared across plots) can also be defined when setting up the figure:

```python
sns.JointGrid(xlim=(-2, 5), ylim=(0, 10))
```
