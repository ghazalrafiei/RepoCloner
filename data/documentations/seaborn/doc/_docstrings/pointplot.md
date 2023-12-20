```python
import seaborn as sns
sns.set_theme(style="whitegrid")
penguins = sns.load_dataset("penguins")
flights = sns.load_dataset("flights")
```
Group by a categorical variable and plot aggregated values, with confidence intervals:

```python
sns.pointplot(data=penguins, x="island", y="body_mass_g")
```
Add a second layer of grouping and differentiate with color:

```python
sns.pointplot(data=penguins, x="island", y="body_mass_g", hue="sex")
```
Redundantly code the `hue` variable using the markers and linestyles for better accessibility:

```python
sns.pointplot(
    data=penguins,
    x="island", y="body_mass_g", hue="sex",
    markers=["o", "s"], linestyles=["-", "--"],
)
```
Use the error bars to represent the standard deviation of each distribution:

```python
sns.pointplot(data=penguins, x="island", y="body_mass_g", errorbar="sd")
```
Customize the appearance of the plot:

```python
sns.pointplot(
    data=penguins, x="body_mass_g", y="island",
    errorbar=("pi", 100), capsize=.4,
    color=".5", linestyle="none", marker="D",
)
```
"Dodge" the artists along the categorical axis to reduce overplotting:

```python
sns.pointplot(data=penguins, x="sex", y="bill_depth_mm", hue="species", dodge=True)
```
Dodge by a specific amount, relative to the width allotted for each level:

```python
sns.stripplot(
    data=penguins, x="species", y="bill_depth_mm", hue="sex",
    dodge=True, alpha=.2, legend=False,
)
sns.pointplot(
    data=penguins, x="species", y="bill_depth_mm", hue="sex",
    dodge=.4, linestyle="none", errorbar=None,
    marker="_", markersize=20, markeredgewidth=3,
)
```
When variables are not explicitly assigned and the dataset is two-dimensional, the plot will aggregate over each column:

```python
flights_wide = flights.pivot(index="year", columns="month", values="passengers")
sns.pointplot(flights_wide)
```
With one-dimensional data, each value is plotted (relative to its key or index when available):

```python
sns.pointplot(flights_wide["Jun"])
```
Control the formatting of the categorical variable as it appears in the tick labels:

```python
sns.pointplot(flights_wide["Jun"], formatter=lambda x: f"'{x % 1900}")
```
Or preserve the native scale of the grouping variable:

```python
ax = sns.pointplot(flights_wide["Jun"], native_scale=True)
ax.plot(1955, 335, marker="*", color="r", markersize=10)
```


```python

```
