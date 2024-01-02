```python
import seaborn.objects as so
from seaborn import load_dataset
penguins = load_dataset("penguins")
```
For discrete or categorical variables, this stat is commonly combined with a :class:`Bar` mark:

```python
so.Plot(penguins, "island").add(so.Bar(), so.Hist())
```
When used to estimate a univariate distribution, it is better to use the :class:`Bars` mark:

```python
p = so.Plot(penguins, "flipper_length_mm")
p.add(so.Bars(), so.Hist())
```
The granularity of the bins will influence whether the underlying distribution is accurately represented. Adjust it by setting the total number:

```python
p.add(so.Bars(), so.Hist(bins=20))
```
Alternatively, specify the *width* of the bins:

```python
p.add(so.Bars(), so.Hist(binwidth=5))
```
By default, the transform returns the count of observations in each bin. The counts can be normalized, e.g. to show a proportion:

```python
p.add(so.Bars(), so.Hist(stat="proportion"))
```
When additional variables define groups, the default behavior is to normalize across all groups:

```python
p = p.facet("island")
p.add(so.Bars(), so.Hist(stat="proportion"))
```
Pass `common_norm=False` to normalize each distribution independently:

```python
p.add(so.Bars(), so.Hist(stat="proportion", common_norm=False))
```
Or, with more than one grouping varible, specify a subset to normalize within:

```python
p.add(so.Bars(), so.Hist(stat="proportion", common_norm=["col"]), color="sex")
```
When distributions overlap it may be easier to discern their shapes with an :class:`Area` mark:

```python
p.add(so.Area(), so.Hist(), color="sex")
```
Or add :class:`Stack` move to represent a part-whole relationship:

```python
p.add(so.Bars(), so.Hist(), so.Stack(), color="sex")
```


```python

```
