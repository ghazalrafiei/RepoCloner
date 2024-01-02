```python
import seaborn.objects as so
from seaborn import load_dataset
healthexp = load_dataset("healthexp").sort_values(["Country", "Year"])
```
Unlike :class:`Line`, this mark does not sort observations before plotting, making it suitable for plotting trajectories through a variable space:

```python
p = so.Plot(healthexp, "Spending_USD", "Life_Expectancy", color="Country")
p.add(so.Path())
```
It otherwise offers the same set of options, including a number of properties that can be set or mapped:

```python
p.add(so.Path(marker="o", pointsize=2, linewidth=.75, fillcolor="w"))
```


```python

```
