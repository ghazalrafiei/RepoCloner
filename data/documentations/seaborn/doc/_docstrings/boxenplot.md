```python
import seaborn as sns
sns.set_theme(style="whitegrid")
diamonds = sns.load_dataset("diamonds")
```
Draw a single horizontal plot, assigning the data directly to the coordinate variable:

```python
sns.boxenplot(x=diamonds["price"])
```
Group by a categorical variable, referencing columns in a datafame

```python
sns.boxenplot(data=diamonds, x="price", y="clarity")
```
Group by another variable, representing it by the color of the boxes. By default, each boxen plot will be "dodged" so that they don't overlap; you can also add a small gap between them:

```python
large_diamond = diamonds["carat"].gt(1).rename("large_diamond")
sns.boxenplot(data=diamonds, x="price", y="clarity", hue=large_diamond, gap=.2)
```
The default rule for choosing each box width represents the percentile covered by the box. Alternatively, you can reduce each box width by a linear factor:

```python
sns.boxenplot(data=diamonds, x="price", y="clarity", width_method="linear")
```
The `width` parameter itself, on the other hand, determines the width of the largest box:

```python
sns.boxenplot(data=diamonds, x="price", y="clarity", width=.5)
```
There are several different approaches for choosing the number of boxes to draw, including a rule based on the confidence level of the percentie estimate:

```python
sns.boxenplot(data=diamonds, x="price", y="clarity", k_depth="trustworthy", trust_alpha=0.01)
```
The `linecolor` and `linewidth` parameters control the outlines of the boxes, while the `line_kws` parameter controls the line representing the median and the `flier_kws` parameter controls the appearance of the outliers:

```python
sns.boxenplot(
    data=diamonds, x="price", y="clarity",
    linewidth=.5, linecolor=".7",
    line_kws=dict(linewidth=1.5, color="#cde"),
    flier_kws=dict(facecolor=".7", linewidth=.5),
)
```
It is also possible to draw unfilled boxes. With unfilled boxes, all elements will be drawn as line art and follow `hue`, when used:

```python
sns.boxenplot(data=diamonds, x="price", y="clarity", hue="clarity", fill=False)
```


```python

```
