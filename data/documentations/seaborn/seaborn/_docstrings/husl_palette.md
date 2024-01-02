```python
import seaborn as sns
sns.set_theme()
sns.palettes._patch_colormap_display()
```
By default, return 6 colors with identical lightness and saturation and evenly-sampled hues:

```python
sns.husl_palette()
```
Increase the number of colors:

```python
sns.husl_palette(8)
```
Decrease the lightness:

```python
sns.husl_palette(l=.4)
```
Decrease the saturation:

```python
sns.husl_palette(s=.4)
```
Change the start-point for hue sampling:

```python
sns.husl_palette(h=.5)
```
Return a continuous colormap:

```python
sns.husl_palette(as_cmap=True)
```


```python

```
