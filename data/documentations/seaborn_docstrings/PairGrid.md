```python
import seaborn as sns; sns.set_theme()
import matplotlib.pyplot as plt
```
Calling the constructor sets up a blank grid of subplots with each row and one column corresponding to a numeric variable in the dataset:

```python
penguins = sns.load_dataset("penguins")
g = sns.PairGrid(penguins)
```
Passing a bivariate function to :meth:`PairGrid.map` will draw a bivariate plot on every axes:

```python
g = sns.PairGrid(penguins)
g.map(sns.scatterplot)
```
Passing separate functions to :meth:`PairGrid.map_diag` and :meth:`PairGrid.map_offdiag` will show each variable's marginal distribution on the diagonal:

```python
g = sns.PairGrid(penguins)
g.map_diag(sns.histplot)
g.map_offdiag(sns.scatterplot)
```
It's also possible to use different functions on the upper and lower triangles of the plot (which are otherwise redundant):

```python
g = sns.PairGrid(penguins, diag_sharey=False)
g.map_upper(sns.scatterplot)
g.map_lower(sns.kdeplot)
g.map_diag(sns.kdeplot)
```
Or to avoid the redundancy altogether:

```python
g = sns.PairGrid(penguins, diag_sharey=False, corner=True)
g.map_lower(sns.scatterplot)
g.map_diag(sns.kdeplot)
```
The :class:`PairGrid` constructor accepts a ``hue`` variable. This variable is passed directly to functions that understand it:

```python
g = sns.PairGrid(penguins, hue="species")
g.map_diag(sns.histplot)
g.map_offdiag(sns.scatterplot)
g.add_legend()
```
But you can also pass matplotlib functions, in which case a groupby is performed internally and a separate plot is drawn for each level:

```python
g = sns.PairGrid(penguins, hue="species")
g.map_diag(plt.hist)
g.map_offdiag(plt.scatter)
g.add_legend()
```
Additional semantic variables can be assigned by passing data vectors directly while mapping the function:

```python
g = sns.PairGrid(penguins, hue="species")
g.map_diag(sns.histplot)
g.map_offdiag(sns.scatterplot, size=penguins["sex"])
g.add_legend(title="", adjust_subtitles=True)
```
When using seaborn functions that can implement a numeric hue mapping, you will want to disable mapping of the variable on the diagonal axes. Note that the ``hue`` variable is excluded from the list of variables shown by default:

```python
g = sns.PairGrid(penguins, hue="body_mass_g")
g.map_diag(sns.histplot, hue=None, color=".3")
g.map_offdiag(sns.scatterplot)
g.add_legend()
```
The ``vars`` parameter can be used to control exactly which variables are used:

```python
variables = ["body_mass_g", "bill_length_mm", "flipper_length_mm"]
g = sns.PairGrid(penguins, hue="body_mass_g", vars=variables)
g.map_diag(sns.histplot, hue=None, color=".3")
g.map_offdiag(sns.scatterplot)
g.add_legend()
```
The plot need not be square: separate variables can be used to define the rows and columns:

```python
x_vars = ["body_mass_g", "bill_length_mm", "bill_depth_mm", "flipper_length_mm"]
y_vars = ["body_mass_g"]
g = sns.PairGrid(penguins, hue="species", x_vars=x_vars, y_vars=y_vars)
g.map_diag(sns.histplot, color=".3")
g.map_offdiag(sns.scatterplot)
g.add_legend()
```
It can be useful to explore different approaches to resolving multiple distributions on the diagonal axes:

```python
g = sns.PairGrid(penguins, hue="species")
g.map_diag(sns.histplot, multiple="stack", element="step")
g.map_offdiag(sns.scatterplot)
g.add_legend()
```


```python

```
