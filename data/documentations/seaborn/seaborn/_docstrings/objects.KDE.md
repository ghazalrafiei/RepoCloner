```python
import seaborn.objects as so
from seaborn import load_dataset
penguins = load_dataset("penguins")
```
This stat estimates transforms observations into a smooth function representing the estimated density:

```python
p = so.Plot(penguins, x="flipper_length_mm")
p.add(so.Area(), so.KDE())
```
Adjust the smoothing bandwidth to see more or fewer details:

```python
p.add(so.Area(), so.KDE(bw_adjust=0.25))
```
The curve will extend beyond observed values in the dataset:

```python
p2 = p.add(so.Bars(alpha=.3), so.Hist("density"))
p2.add(so.Line(), so.KDE())
```
Control the range of the density curve relative to the observations using `cut`:

```python
p2.add(so.Line(), so.KDE(cut=0))
```
When observations are assigned to the `y` variable, the density will be shown for `x`:

```python
so.Plot(penguins, y="flipper_length_mm").add(so.Area(), so.KDE())
```
Use `gridsize` to increase or decrease the resolution of the grid where the density is evaluated:

```python
p.add(so.Dots(), so.KDE(gridsize=100))
```
Or pass `None` to evaluate the density at the original datapoints:

```python
p.add(so.Dots(), so.KDE(gridsize=None))
```
Other variables will define groups for the estimation:

```python
p.add(so.Area(), so.KDE(), color="species")
```
By default, the density is normalized across all groups (i.e., the joint density is shown); pass `common_norm=False` to show conditional densities:

```python
p.add(so.Area(), so.KDE(common_norm=False), color="species")
```
Or pass a list of variables to condition on:

```python
(
    p.facet("sex")
    .add(so.Area(), so.KDE(common_norm=["col"]), color="species")
)
```
This stat can be combined with other transforms, such as :class:`Stack` (when `common_grid=True`):

```python
p.add(so.Area(), so.KDE(), so.Stack(), color="sex")
```
Set `cumulative=True` to integrate the density:

```python
p.add(so.Line(), so.KDE(cumulative=True))
```


```python

```
