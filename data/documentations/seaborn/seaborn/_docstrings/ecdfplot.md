Plot a univariate distribution along the x axis:


```python
import seaborn as sns; sns.set_theme()
```


```python
penguins = sns.load_dataset("penguins")
sns.ecdfplot(data=penguins, x="flipper_length_mm")
```

Flip the plot by assigning the data variable to the y axis:


```python
sns.ecdfplot(data=penguins, y="flipper_length_mm")
```

If neither `x` nor `y` is assigned, the dataset is treated as wide-form, and a histogram is drawn for each numeric column:


```python
sns.ecdfplot(data=penguins.filter(like="bill_", axis="columns"))
```

You can also draw multiple histograms from a long-form dataset with hue mapping:


```python
sns.ecdfplot(data=penguins, x="bill_length_mm", hue="species")
```

The default distribution statistic is normalized to show a proportion, but you can show absolute counts or percents instead:


```python
sns.ecdfplot(data=penguins, x="bill_length_mm", hue="species", stat="count")
```

It's also possible to plot the empirical complementary CDF (1 - CDF):


```python
sns.ecdfplot(data=penguins, x="bill_length_mm", hue="species", complementary=True)
```


```python

```
