```python
import seaborn as sns
sns.set_theme(style="whitegrid")
titanic = sns.load_dataset("titanic")
```
Draw a single horizontal boxplot, assigning the data directly to the coordinate variable:

```python
sns.boxplot(x=titanic["age"])
```
Group by a categorical variable, referencing columns in a dataframe:

```python
sns.boxplot(data=titanic, x="age", y="class")
```
Draw a vertical boxplot with nested grouping by two variables:

```python
sns.boxplot(data=titanic, x="class", y="age", hue="alive")
```
Draw the boxes as line art and add a small gap between them:

```python
sns.boxplot(data=titanic, x="class", y="age", hue="alive", fill=False, gap=.1)
```
Cover the full range of the data with the whiskers:

```python
sns.boxplot(data=titanic, x="age", y="deck", whis=(0, 100))
```
Draw narrower boxes:

```python
sns.boxplot(data=titanic, x="age", y="deck", width=.5)
```
Modify the color and width of all the line artists:

```python
sns.boxplot(data=titanic, x="age", y="deck", color=".8", linecolor="#137", linewidth=.75)
```

Group by a numeric variable and preserve its native scaling:


```python
ax = sns.boxplot(x=titanic["age"].round(-1), y=titanic["fare"], native_scale=True)
ax.axvline(25, color=".3", dashes=(2, 2))
```
Customize the plot using parameters of the underlying matplotlib function:

```python
sns.boxplot(
    data=titanic, x="age", y="class",
    notch=True, showcaps=False,
    flierprops={"marker": "x"},
    boxprops={"facecolor": (.3, .5, .7, .5)},
    medianprops={"color": "r", "linewidth": 2},
)
```


```python

```
