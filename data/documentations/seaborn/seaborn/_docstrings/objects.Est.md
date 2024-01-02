```python
import seaborn.objects as so
from seaborn import load_dataset
diamonds = load_dataset("diamonds")
```
The default behavior is to compute the mean and 95% confidence interval (using bootstrapping):

```python
p = so.Plot(diamonds, "clarity", "carat")
p.add(so.Range(), so.Est())
```
Other estimators may be selected by name if they are pandas methods:

```python
p.add(so.Range(), so.Est("median"))
```
There are several options for computing the error bar interval, such as (scaled) standard errors:

```python
p.add(so.Range(), so.Est(errorbar="se"))
```
The error bars can also represent the spread of the distribution around the estimate using (scaled) standard deviations:

```python
p.add(so.Range(), so.Est(errorbar="sd"))
```
Because confidence intervals are computed using bootstrapping, there will be small amounts of randomness. Reduce the random variability by increasing the nubmer of bootstrap iterations (although this will be slower), or eliminate it by seeding the random number generator:

```python
p.add(so.Range(), so.Est(seed=0))
```

To compute a weighted estimate (and confidence interval), assign a `weight` variable in the layer where you use the stat:


```python
p.add(so.Range(), so.Est(), weight="price")
```


```python

```
