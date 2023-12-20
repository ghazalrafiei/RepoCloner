```python
import seaborn as sns
sns.set_theme(style="white")
```
Assign a variable to ``x`` to plot a univariate distribution along the x axis:

```python
penguins = sns.load_dataset("penguins")
sns.histplot(data=penguins, x="flipper_length_mm")
```

Flip the plot by assigning the data variable to the y axis:


```python
sns.histplot(data=penguins, y="flipper_length_mm")
```

Check how well the histogram represents the data by specifying a different bin width:


```python
sns.histplot(data=penguins, x="flipper_length_mm", binwidth=3)
```

You can also define the total number of bins to use:


```python
sns.histplot(data=penguins, x="flipper_length_mm", bins=30)
```

Add a kernel density estimate to smooth the histogram, providing complementary information about the shape of the distribution:


```python
sns.histplot(data=penguins, x="flipper_length_mm", kde=True)
```

If neither `x` nor `y` is assigned, the dataset is treated as wide-form, and a histogram is drawn for each numeric column:


```python
sns.histplot(data=penguins)
```

You can otherwise draw multiple histograms from a long-form dataset with hue mapping:


```python
sns.histplot(data=penguins, x="flipper_length_mm", hue="species")
```

The default approach to plotting multiple distributions is to "layer" them, but you can also "stack" them:


```python
sns.histplot(data=penguins, x="flipper_length_mm", hue="species", multiple="stack")
```

Overlapping bars can be hard to visually resolve. A different approach would be to draw a step function:


```python
sns.histplot(penguins, x="flipper_length_mm", hue="species", element="step")
```

You can move even farther away from bars by drawing a polygon with vertices in the center of each bin. This may make it easier to see the shape of the distribution, but use with caution: it will be less obvious to your audience that they are looking at a histogram:


```python
sns.histplot(penguins, x="flipper_length_mm", hue="species", element="poly")
```

To compare the distribution of subsets that differ substantially in size, use independent density normalization:


```python
sns.histplot(
    penguins, x="bill_length_mm", hue="island", element="step",
    stat="density", common_norm=False,
)
```

It's also possible to normalize so that each bar's height shows a probability, proportion, or percent, which make more sense for discrete variables:


```python
tips = sns.load_dataset("tips")
sns.histplot(data=tips, x="size", stat="percent", discrete=True)
```

You can even draw a histogram over categorical variables (although this is an experimental feature):


```python
sns.histplot(data=tips, x="day", shrink=.8)
```

When using a ``hue`` semantic with discrete data, it can make sense to "dodge" the levels:


```python
sns.histplot(data=tips, x="day", hue="sex", multiple="dodge", shrink=.8)
```
Real-world data is often skewed. For heavily skewed distributions, it's better to define the bins in log space. Compare:

```python
planets = sns.load_dataset("planets")
sns.histplot(data=planets, x="distance")
```

To the log-scale version:


```python
sns.histplot(data=planets, x="distance", log_scale=True)
```

There are also a number of options for how the histogram appears. You can show unfilled bars:


```python
sns.histplot(data=planets, x="distance", log_scale=True, fill=False)
```

Or an unfilled step function:


```python
sns.histplot(data=planets, x="distance", log_scale=True, element="step", fill=False)
```

Step functions, especially when unfilled, make it easy to compare cumulative histograms:


```python
sns.histplot(
    data=planets, x="distance", hue="method",
    hue_order=["Radial Velocity", "Transit"],
    log_scale=True, element="step", fill=False,
    cumulative=True, stat="density", common_norm=False,
)
```

When both ``x`` and ``y`` are assigned, a bivariate histogram is computed and shown as a heatmap:


```python
sns.histplot(penguins, x="bill_depth_mm", y="body_mass_g")
```

It's possible to assign a ``hue`` variable too, although this will not work well if data from the different levels have substantial overlap:


```python
sns.histplot(penguins, x="bill_depth_mm", y="body_mass_g", hue="species")
```

Multiple color maps can make sense when one of the variables is discrete:


```python
sns.histplot(
    penguins, x="bill_depth_mm", y="species", hue="species", legend=False
)
```

The bivariate histogram accepts all of the same options for computation as its univariate counterpart, using tuples to parametrize ``x`` and ``y`` independently:


```python
sns.histplot(
    planets, x="year", y="distance",
    bins=30, discrete=(True, False), log_scale=(False, True),
)
```

The default behavior makes cells with no observations transparent, although this can be disabled: 


```python
sns.histplot(
    planets, x="year", y="distance",
    bins=30, discrete=(True, False), log_scale=(False, True),
    thresh=None,
)
```

It's also possible to set the threshold and colormap saturation point in terms of the proportion of cumulative counts:


```python
sns.histplot(
    planets, x="year", y="distance",
    bins=30, discrete=(True, False), log_scale=(False, True),
    pthresh=.05, pmax=.9,
)
```

To annotate the colormap, add a colorbar:


```python
sns.histplot(
    planets, x="year", y="distance",
    bins=30, discrete=(True, False), log_scale=(False, True),
    cbar=True, cbar_kws=dict(shrink=.75),
)
```
