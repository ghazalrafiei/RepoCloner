```python
import seaborn.objects as so
from seaborn import load_dataset
healthexp = load_dataset("healthexp")
```
By default, this transform scales each group relative to its maximum value:

```python
(
    so.Plot(healthexp, x="Year", y="Spending_USD", color="Country")
    .add(so.Lines(), so.Norm())
    .label(y="Spending relative to maximum amount")
)
```
Use `where` to constrain the values used to define a baseline, and `percent` to scale the output:

```python
(
    so.Plot(healthexp, x="Year", y="Spending_USD", color="Country")
    .add(so.Lines(), so.Norm(where="x == x.min()", percent=True))
    .label(y="Percent change in spending from 1970 baseline")
)
```


```python

```
