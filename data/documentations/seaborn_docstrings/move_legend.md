```python
import seaborn as sns
sns.set_theme()
penguins = sns.load_dataset("penguins")
```
For axes-level functions, pass the :class:`matplotlib.axes.Axes` object and provide a new location.

```python
ax = sns.histplot(penguins, x="bill_length_mm", hue="species")
sns.move_legend(ax, "center right")
```
Use the `bbox_to_anchor` parameter for more fine-grained control, including moving the legend outside of the axes:

```python
ax = sns.histplot(penguins, x="bill_length_mm", hue="species")
sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
```
Pass additional :meth:`matplotlib.axes.Axes.legend` parameters to update other properties:

```python
ax = sns.histplot(penguins, x="bill_length_mm", hue="species")
sns.move_legend(
    ax, "lower center",
    bbox_to_anchor=(.5, 1), ncol=3, title=None, frameon=False,
)
```
It's also possible to move the legend created by a figure-level function. But when fine-tuning the position, you must bear in mind that the figure will have extra blank space on the right:

```python
g = sns.displot(
    penguins,
    x="bill_length_mm", hue="species",
    col="island", col_wrap=2, height=3,
)
sns.move_legend(g, "upper left", bbox_to_anchor=(.55, .45))
```
One way to avoid this would be to set `legend_out=False` on the :class:`FacetGrid`:

```python
g = sns.displot(
    penguins,
    x="bill_length_mm", hue="species",
    col="island", col_wrap=2, height=3,
    facet_kws=dict(legend_out=False),
)
sns.move_legend(g, "upper left", bbox_to_anchor=(.55, .45), frameon=False)
```


```python

```
