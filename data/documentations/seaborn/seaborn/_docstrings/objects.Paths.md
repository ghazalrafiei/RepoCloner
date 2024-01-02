```python
import seaborn.objects as so
from seaborn import load_dataset
networks = (
    load_dataset("brain_networks", header=[0, 1, 2], index_col=0)
    .rename_axis("timepoint")
    .stack([0, 1, 2])
    .groupby(["timepoint", "network", "hemi"])
    .mean()
    .unstack("network")
    .reset_index()
    .query("timepoint < 100")
)
```
Unlike :class:`Lines`, this mark does not sort observations before plotting, making it suitable for plotting trajectories through a variable space:

```python
p = (
    so.Plot(networks)
    .pair(
        x=["5", "8", "12", "15"],
        y=["6", "13", "16"],
    )
    .layout(size=(8, 5))
    .share(x=True, y=True)
)
p.add(so.Paths())
```
The mark has the same set of properties as :class:`Lines`:

```python
p.add(so.Paths(linewidth=1, alpha=.8), color="hemi")
```


```python

```
