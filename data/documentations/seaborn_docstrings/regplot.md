```python
import numpy as np
import seaborn as sns
sns.set_theme()
mpg = sns.load_dataset("mpg")
```
Plot the relationship between two variables in a DataFrame:

```python
sns.regplot(data=mpg, x="weight", y="acceleration")
```
Fit a higher-order polynomial regression to capture nonlinear trends:

```python
sns.regplot(data=mpg, x="weight", y="mpg", order=2)
```
Alternatively, fit a log-linear regression:

```python
sns.regplot(data=mpg, x="displacement", y="mpg", logx=True)
```
Or use a locally-weighted (LOWESS) smoother:

```python
sns.regplot(data=mpg, x="horsepower", y="mpg", lowess=True)
```
Fit a logistic regression when the response variable is binary:

```python
sns.regplot(x=mpg["weight"], y=mpg["origin"].eq("usa").rename("from_usa"), logistic=True)
```
Fit a robust regression to downweight the influence of outliers:

```python
sns.regplot(data=mpg, x="horsepower", y="weight", robust=True)
```
Disable the confidence interval for faster plotting:

```python
sns.regplot(data=mpg, x="weight", y="horsepower", ci=None)
```
Jitter the scatterplot when the `x` variable is discrete:

```python
sns.regplot(data=mpg, x="cylinders", y="weight", x_jitter=.15)
```
Or aggregate over the distinct `x` values:

```python
sns.regplot(data=mpg, x="cylinders", y="acceleration", x_estimator=np.mean, order=2)
```
With a continuous `x` variable, bin and then aggregate:

```python
sns.regplot(data=mpg, x="weight", y="mpg", x_bins=np.arange(2000, 5500, 250), order=2)
```
Customize the appearance of various elements:

```python
sns.regplot(
    data=mpg, x="weight", y="horsepower",
    ci=99, marker="x", color=".3", line_kws=dict(color="r"),
)
```


```python

```
