```python
import seaborn as sns
sns.set_theme()
```
Pass a :class:`DataFrame` to plot with indices as row/column labels:

```python
glue = sns.load_dataset("glue").pivot(index="Model", columns="Task", values="Score")
sns.heatmap(glue)
```
Use `annot` to represent the cell values with text:

```python
sns.heatmap(glue, annot=True)
```
Control the annotations with a formatting string:

```python
sns.heatmap(glue, annot=True, fmt=".1f")
```
Use a separate dataframe for the annotations:

```python
sns.heatmap(glue, annot=glue.rank(axis="columns"))
```
Add lines between cells:

```python
sns.heatmap(glue, annot=True, linewidth=.5)
```
Select a different colormap by name:

```python
sns.heatmap(glue, cmap="crest")
```
Or pass a colormap object:

```python
sns.heatmap(glue, cmap=sns.cubehelix_palette(as_cmap=True))
```
Set the colormap norm (data values corresponding to minimum and maximum points):

```python
sns.heatmap(glue, vmin=50, vmax=100)
```
Use methods on the :class:`matplotlib.axes.Axes` object to tweak the plot:

```python
ax = sns.heatmap(glue, annot=True)
ax.set(xlabel="", ylabel="")
ax.xaxis.tick_top()
```
