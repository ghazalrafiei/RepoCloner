```python
import seaborn as sns
sns.set_theme()
```
Plot a heatmap with row and column clustering:

```python
iris = sns.load_dataset("iris")
species = iris.pop("species")
sns.clustermap(iris)
```
Change the size and layout of the figure:

```python
sns.clustermap(
    iris,
    figsize=(7, 5),
    row_cluster=False,
    dendrogram_ratio=(.1, .2),
    cbar_pos=(0, .2, .03, .4)
)
```
Add colored labels to identify observations:

```python
lut = dict(zip(species.unique(), "rbg"))
row_colors = species.map(lut)
sns.clustermap(iris, row_colors=row_colors)
```
Use a different colormap and adjust the limits of the color range:

```python
sns.clustermap(iris, cmap="mako", vmin=0, vmax=10)
```
Use differente clustering parameters:

```python
sns.clustermap(iris, metric="correlation", method="single")
```
Standardize the data within the columns:

```python
sns.clustermap(iris, standard_scale=1)
```
Normalize the data within rows:

```python
sns.clustermap(iris, z_score=0, cmap="vlag", center=0)
```


```python

```
