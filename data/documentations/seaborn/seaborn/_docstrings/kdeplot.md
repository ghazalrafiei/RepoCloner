```python
import seaborn as sns; sns.set_theme()
```

Plot a univariate distribution along the x axis:


```python
tips = sns.load_dataset("tips")
sns.kdeplot(data=tips, x="total_bill")
```

Flip the plot by assigning the data variable to the y axis:


```python
sns.kdeplot(data=tips, y="total_bill")
```

Plot distributions for each column of a wide-form dataset:


```python
iris = sns.load_dataset("iris")
sns.kdeplot(data=iris)
```

Use less smoothing:


```python
sns.kdeplot(data=tips, x="total_bill", bw_adjust=.2)
```

Use more smoothing, but don't smooth past the extreme data points:


```python
ax= sns.kdeplot(data=tips, x="total_bill", bw_adjust=5, cut=0)
```

Plot conditional distributions with hue mapping of a second variable:


```python
sns.kdeplot(data=tips, x="total_bill", hue="time")
```

"Stack" the conditional distributions:


```python
sns.kdeplot(data=tips, x="total_bill", hue="time", multiple="stack")
```

Normalize the stacked distribution at each value in the grid:


```python
sns.kdeplot(data=tips, x="total_bill", hue="time", multiple="fill")
```

Estimate the cumulative distribution function(s), normalizing each subset:


```python
sns.kdeplot(
    data=tips, x="total_bill", hue="time",
    cumulative=True, common_norm=False, common_grid=True,
)
```

Estimate distribution from aggregated data, using weights:


```python
tips_agg = (tips
    .groupby("size")
    .agg(total_bill=("total_bill", "mean"), n=("total_bill", "count"))
)
sns.kdeplot(data=tips_agg, x="total_bill", weights="n")
```

Map the data variable with log scaling:


```python
diamonds = sns.load_dataset("diamonds")
sns.kdeplot(data=diamonds, x="price", log_scale=True)
```

Use numeric hue mapping:


```python
sns.kdeplot(data=tips, x="total_bill", hue="size")
```

Modify the appearance of the plot:


```python
sns.kdeplot(
   data=tips, x="total_bill", hue="size",
   fill=True, common_norm=False, palette="crest",
   alpha=.5, linewidth=0,
)
```

Plot a bivariate distribution:


```python
geyser = sns.load_dataset("geyser")
sns.kdeplot(data=geyser, x="waiting", y="duration")
```

Map a third variable with a hue semantic to show conditional distributions:


```python
sns.kdeplot(data=geyser, x="waiting", y="duration", hue="kind")
```

Show filled contours:


```python
sns.kdeplot(
    data=geyser, x="waiting", y="duration", hue="kind", fill=True,
)
```

Show fewer contour levels, covering less of the distribution:


```python
sns.kdeplot(
    data=geyser, x="waiting", y="duration", hue="kind",
    levels=5, thresh=.2,
)
```

Fill the axes extent with a smooth distribution, using a different colormap:


```python
sns.kdeplot(
    data=geyser, x="waiting", y="duration",
    fill=True, thresh=0, levels=100, cmap="mako",
)
```
