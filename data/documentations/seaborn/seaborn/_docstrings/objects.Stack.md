```python
import seaborn.objects as so
from seaborn import load_dataset
titanic = load_dataset("titanic").sort_values("alive", ascending=False)
```
This transform applies a vertical shift to eliminate overlap between marks with a baseline, such as :class:`Bar` or :class:`Area`:

```python
so.Plot(titanic, x="class", color="sex").add(so.Bar(), so.Count(), so.Stack())
```
Stacking can make it much harder to compare values between groups that get shifted, but it can work well when depicting a part-whole relationship:

```python
(
    so.Plot(titanic, x="age", alpha="alive")
    .facet("sex")
    .add(so.Bars(), so.Hist(binwidth=10), so.Stack())
)
```


```python

```
