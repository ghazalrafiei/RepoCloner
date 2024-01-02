```python
import seaborn as sns
sns.set_theme(style="whitegrid")
```
The default violinplot represents a distribution two ways: a patch showing a symmetric kernel density estimate (KDE), and the quartiles / whiskers of a box plot:

```python
df = sns.load_dataset("titanic")
sns.violinplot(x=df["age"])
```
In a bivariate plot, one of the variables will "group" so that multiple violins are drawn:

```python
sns.violinplot(data=df, x="age", y="class")
```
By default, the orientation of the plot is determined by the variable types, preferring to group by a categorical variable:

```python
sns.violinplot(data=df, x="class", y="age", hue="alive")
```
Pass `fill=False` to draw line-art violins:

```python
sns.violinplot(data=df, x="class", y="age", hue="alive", fill=False)
```
Draw "split" violins to take up less space, and only show the data quarties:

```python
sns.violinplot(data=df, x="class", y="age", hue="alive", split=True, inner="quart")
```
Add a small gap between the dodged violins:

```python
sns.violinplot(data=df, x="class", y="age", hue="alive", split=True, gap=.1, inner="quart")
```
Starting in version 0.13.0, it is possilbe to "split" single violins:

```python
sns.violinplot(data=df, x="class", y="age", split=True, inner="quart")
```
Represent every observation inside the distribution by setting `inner="stick"` or `inner="point"`:

```python
sns.violinplot(data=df, x="age", y="deck", inner="point")
```
Normalize the width of each violin to represent the number of observations:

```python
sns.violinplot(data=df, x="age", y="deck", inner="point", density_norm="count")
```
By default, the KDE will smooth past the extremes of the observed data; set `cut=0` to prevent this:

```python
sns.violinplot(data=df, x="age", y="alive", cut=0, inner="stick")
```
The `bw_adjust` parameter controls the amount of smoothing:

```python
sns.violinplot(data=df, x="age", y="alive", bw_adjust=.5, inner="stick")
```
By default, the violins are drawn at fixed positions on a categorical scale, even if the grouping variable is numeric. Starting in version 0.13.0, pass the `native_scale=True` parameter to preserve the original scale on both axes:

```python
sns.violinplot(x=df["age"].round(-1) + 5, y=df["fare"], native_scale=True)
```
When using a categorical scale, the `formatter` parameter accepts a function that defines categories:

```python
decades = lambda x: f"{int(x)}–{int(x + 10)}"
sns.violinplot(x=df["age"].round(-1), y=df["fare"], formatter=decades)
```
By default, the "inner" representation scales with the `linewidth` and `linecolor` parameters:

```python
sns.violinplot(data=df, x="age", linewidth=1, linecolor="k")
```
Use `inner_kws` to pass parameters directly to the inner plotting functions:

```python
sns.violinplot(data=df, x="age", inner_kws=dict(box_width=15, whis_width=2, color=".8"))
```


```python

```
