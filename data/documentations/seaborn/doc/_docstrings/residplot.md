```python
import seaborn as sns
sns.set_theme()
mpg = sns.load_dataset("mpg")
```
Pass `x` and `y` to see a scatter plot of the residuals after fitting a simple regression model:

```python
sns.residplot(data=mpg, x="weight", y="displacement")
```
Structure in the residual plot can reveal a violation of linear regression assumptions:

```python
sns.residplot(data=mpg, x="horsepower", y="mpg")
```
Remove higher-order trends to test whether that stabilizes the residuals:

```python
sns.residplot(data=mpg, x="horsepower", y="mpg", order=2)
```
Adding a LOWESS curve can help reveal or emphasize structure:

```python
sns.residplot(data=mpg, x="horsepower", y="mpg", lowess=True, line_kws=dict(color="r"))
```
