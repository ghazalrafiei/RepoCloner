```python
import seaborn.objects as so
from seaborn import load_dataset
tips = load_dataset("tips")
```
The transform counts distinct observations of the orientation variable defines a new variable on the opposite axis:

```python
so.Plot(tips, x="day").add(so.Bar(), so.Count())
```
When additional mapping variables are defined, they are also used to define groups:

```python
so.Plot(tips, x="day", color="sex").add(so.Bar(), so.Count(), so.Dodge())
```
Unlike :class:`Hist`, numeric data are not binned before counting:

```python
so.Plot(tips, x="size").add(so.Bar(), so.Count())
```
When the `y` variable is defined, the counts are assigned to the `x` variable:

```python
so.Plot(tips, y="size").add(so.Bar(), so.Count())
```


```python

```
