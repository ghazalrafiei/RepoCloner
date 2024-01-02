```python
import seaborn as sns
sns.set_theme(style="whitegrid")
penguins = sns.load_dataset("penguins")
flights = sns.load_dataset("flights")
```
With long data, assign `x` and `y` to group by a categorical variable and plot aggregated values, with confidence intervals:

```python
sns.barplot(penguins, x="island", y="body_mass_g")
```
Prior to v0.13.0, each bar would have a different color. To replicate this behavior, assign the grouping variable to `hue` as well:

```python
sns.barplot(penguins, x="body_mass_g", y="island", hue="island", legend=False)
```
When plotting a "wide-form" dataframe, each column will be aggregated and represented as a bar:

```python
flights_wide = flights.pivot(index="year", columns="month", values="passengers")
sns.barplot(flights_wide)
```
Passing only a series (or dict) will plot each of its values, using the index (or keys) to label the bars:

```python
sns.barplot(flights_wide["Jun"])
```
With long-form data, you can add a second layer of grouping with `hue`:

```python
sns.barplot(penguins, x="island", y="body_mass_g", hue="sex")
```
Use the error bars to show the standard deviation rather than a confidence interval:

```python
sns.barplot(penguins, x="island", y="body_mass_g", errorbar="sd")
```
Use a different aggregation function and disable the error bars:

```python
sns.barplot(flights, x="year", y="passengers", estimator="sum", errorbar=None)
```
Add text labels with each bar's value:

```python
ax = sns.barplot(flights, x="year", y="passengers", estimator="sum", errorbar=None)
ax.bar_label(ax.containers[0], fontsize=10);
```
Preserve the original scaling of the grouping variable and add annotations in numeric coordinates:

```python
ax = sns.barplot(
    flights, x="year", y="passengers",
    native_scale=True,
    estimator="sum", errorbar=None,
)
ax.plot(1955, 3600, "*", markersize=10, color="r")
```
Use `orient` to resolve ambiguity about which variable should group when both are numeric:

```python
sns.barplot(flights, x="passengers", y="year", orient="y")
```
Customize the appearance of the plot using :class:`matplotlib.patches.Rectangle` and :class:`matplotlib.lines.Line2D` keyword arguments:

```python
sns.barplot(
    penguins, x="body_mass_g", y="island",
    errorbar=("pi", 50), capsize=.4,
    err_kws={"color": ".5", "linewidth": 2.5},
    linewidth=2.5, edgecolor=".5", facecolor=(0, 0, 0, 0),
)
```
Use :func:`catplot` to draw faceted bars, which is recommended over working directly with :class:`FacetGrid`:

```python
sns.catplot(
    penguins, kind="bar",
    x="sex", y="body_mass_g", col="species",
    height=4, aspect=.5,
)
```


```python

```
